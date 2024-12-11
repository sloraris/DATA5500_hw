import base64
from collections import defaultdict
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt
import os
import pandas as pd
import requests
import seaborn as sns
import yaml

# read_config
# __init__
# create_auth_header
# test_adguard
# query_adguard_stats
# query_adguard_logs
# analyze_all_patterns
# analyze_temporal_patterns
# analyze_client_behavior
# analyze_domain_patterns
# visualize_logs_data
# generate_stats_html_report
# generate_logs_html_report

# Read server YAML file
def read_config(file_name):
    file_path = os.getcwd()
    config_file = f"{file_path}/{file_name}"
    print(f"Looking for file at: {config_file}")  # debug print
    try:
        with open(config_file, 'r') as file:
            servers = yaml.safe_load(file) # load YAML server config to keep server info secure and flexible
            print() # for formatting
            for server in servers:
                print(f"Loaded server: {server['name']}")  # debug print
            print() # also for formatting
            return servers
    except FileNotFoundError:
        print(f"Error: server file {config_file} not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None


class AdGuardAnalyzer:
    # Initialize an AdGuard Home instance
    def __init__(self, server, output):
        print(f"Initializing {server['name']}...")

        # Set server info
        self.name = server['name']
        self.base_url = server['base_url']
        self.timeframe = int(server['timeframe'])
        self.auth = self.create_auth_header(server)

        # Set server data storage locations
        self.output_dir = os.path.join(os.getcwd(), output)
        self.plots_dir = os.path.join(self.output_dir, "plots")
        self.reports_dir = os.path.join(self.output_dir, "reports")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.plots_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)

        # Test connection and get initial stats
        if self.test_adguard():
            print("Getting data...")
            self.stats_data = self.query_adguard_stats()
            self.logs_data = self.query_adguard_logs(self.timeframe)
            if self.logs_data and self.stats_data:
                self.analyze_stats_data()
                self.analyze_all_patterns()


    # Create authorization header required by AdGuard Home API
    def create_auth_header(self, server):
        credentials = f"{server['username']}:{server['password']}" # AdGuard Home requires username and password be submitted in this format
        encoded_credentials = base64.b64encode(credentials.encode()).decode() # Adguard Home also requires credentials to be base64 encoded
        print(f"Created auth header for {server['name']}")
        return {"Authorization": f"Basic {encoded_credentials}"}

    # Test connection
    def test_adguard(self):
        try:
            print(f"Attempting to connect to {self.name}...")
            response = requests.get(f"{self.base_url}/status", headers=self.auth) # test api
            test = response.json() # convert response to json
            print(f"Connected to {self.name} successfully!\n")
            print(f"Version - {test['version']}\nRunning - {test['running']}\nDNS Port - {test['dns_port']}\n")
            response.raise_for_status()
            return test
        except KeyError as e:
            print("Connection failed.")
            print(f"Missing required field in server configuration: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print("Connection failed.")
            print(f"Error connecting to API: {e}")
            return None

    # Get AdGuard stats
    def query_adguard_stats(self):
        print(f"Retrieving AdGuard stats for {self.name}...")
        response = requests.get(f"{self.base_url}/stats", headers=self.auth) # get stats
        stats_response = response.json() # convert to json
        stats = { # list of stats to report
            "DNS Queries": "num_dns_queries",
            "Most Queried": "top_queried_domains",
            "Blocked Queries": "num_blocked_filtering",
            "Most Blocked": "top_blocked_domains",
            "Most Active Clients": "top_clients"
        }
        for name, key in stats.items(): # formatting for stats report
            match key:
                case key if key.startswith("num_"): # for simple key/value
                    print(f"{name}: {stats_response[key]:,}")
                case key if key.startswith("top_"): # for lists of dictionaries
                    print(f"{name}:")
                    for entry in stats_response[key][:5]:
                        for item, count in entry.items():
                            print(f"- {item}: {count:,}")
                    print()
                case _: # ignore others
                    pass
        with open(f"{self.output_dir}/{self.name}_stats_data.json", "w") as file: # write stats to file
            json.dump(stats_response, file, indent=4)
        return stats_response

    # Get adguard advanced logs and filter for a time-period
    def query_adguard_logs(self, time_span: int) -> dict:
        """Get detailed query log for the last X hours"""
        print(f"Retrieving query log for {self.name}...")

        params = {
            'offset': 0,
            'limit': 100000
        }

        try:
            response = requests.get(
                f"{self.base_url}/querylog",
                headers=self.auth,
                params=params
            )

            # Debug prints
            print(f"URL: {response.url}")
            print(f"Status Code: {response.status_code}")

            # Check if response is successful
            response.raise_for_status()
            data = response.json()

            # Filter queries based on time_span after receiving them
            if 'data' in data:
                end_time = int(datetime.now().timestamp())
                start_time = end_time - (time_span * 3600)  # Convert hours to seconds
                data['data'] = [
                    query for query in data['data']
                    if query.get('time') and
                    datetime.fromisoformat(query['time'].replace('Z', '+00:00')).timestamp() > start_time
                ]
                print(f"Retrieved {len(data['data'])} queries from the last {time_span} hours")

            # Write logs to file
            with open(f"{self.output_dir}/{self.name}_logs_data.json", "w") as file:
                json.dump(data, file, indent=4)

            return data

        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return {'data': []}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print("Full response text:")
            print(response.text)
            return {'data': []}

    def analyze_stats_data(self):
        """Analyze query data and create visualizations"""
        print(f"Analyzing query data for {self.name}...")

        # Convert stats data for visualization
        stats = self.stats_data

        # Create figure with subplots
        plt.style.use('default')
        fig = plt.figure(figsize=(15, 10))

        # 1. DNS Queries vs Blocked Queries
        plt.subplot(2, 2, 1)
        query_types = ['Total DNS Queries', 'Blocked Queries']
        query_counts = [stats['num_dns_queries'], stats['num_blocked_filtering']]
        plt.bar(query_types, query_counts)
        plt.title(f'Query Statistics for {self.name}')
        plt.ylabel('Number of Queries')

        # 2. Top Queried Domains
        plt.subplot(2, 2, 2)
        # Extract domain and count from list of dictionaries
        domains = []
        counts = []
        for entry in stats['top_queried_domains'][:5]:  # Get first 5 entries
            domain = list(entry.keys())[0]   # Get the domain (key)
            count = list(entry.values())[0]  # Get the count (value)
            domains.append(domain)
            counts.append(count)
        plt.barh(domains, counts)
        plt.title('Top 5 Queried Domains')
        plt.xlabel('Number of Queries')

        # 3. Top Blocked Domains
        plt.subplot(2, 2, 3)
        # Extract domain and count from list of dictionaries
        blocked_domains = []
        blocked_counts = []
        for entry in stats['top_blocked_domains'][:5]:  # Get first 5 entries
            domain = list(entry.keys())[0]   # Get the domain (key)
            count = list(entry.values())[0]  # Get the count (value)
            blocked_domains.append(domain)
            blocked_counts.append(count)
        plt.barh(blocked_domains, blocked_counts, color='red')
        plt.title('Top 5 Blocked Domains')
        plt.xlabel('Number of Blocks')

        # 4. Top Clients
        plt.subplot(2, 2, 4)
        # Extract client and count from list of dictionaries
        clients = []
        client_counts = []
        for entry in stats['top_clients'][:5]:  # Get first 5 entries
            client = list(entry.keys())[0]   # Get the client IP (key)
            count = list(entry.values())[0]  # Get the count (value)
            clients.append(client)
            client_counts.append(count)
        plt.pie(client_counts, labels=clients, autopct='%1.1f%%')
        plt.title('Query Distribution by Client')

        plt.tight_layout()
        plt.savefig(f"{self.plots_dir}/{self.name}_stats_analysis.png")
        plt.close()

        # Generate HTML report
        self.generate_stats_html_report()


    def analyze_all_patterns(self):
        """Perform comprehensive analysis of DNS query patterns"""
        print(f"\nPerforming comprehensive analysis for {self.name}...")

        # Get query log data
        time_span = int(self.timeframe)
        queries = self.logs_data
        if not queries or 'data' not in queries:
            print("No query data available for analysis")
            return

        # Perform various analyses
        temporal_analysis = self.analyze_temporal_patterns(queries['data'])
        client_analysis = self.analyze_client_behavior(queries['data'])
        domain_analysis = self.analyze_domain_patterns(queries['data'])

        # Generate visualizations
        self.visualize_temporal_patterns(temporal_analysis)

        # Generate insights
        insights = self.generate_insights_report(time_span)

        # Create comprehensive HTML report
        self.generate_logs_html_report(
            temporal_analysis,
            client_analysis,
            domain_analysis,
            insights,
            time_span
        )


    def analyze_temporal_patterns(self, queries: list) -> dict:
        """Analyze query patterns over time"""
        temporal_analysis = {
            'hourly_distribution': defaultdict(int),
            'query_types_over_time': defaultdict(lambda: defaultdict(int)),
            'blocked_ratio_over_time': defaultdict(lambda: {'total': 0, 'blocked': 0}),
            'client_activity_hours': defaultdict(set)
        }

        for query in queries:
            # Convert ISO timestamp to datetime
            timestamp = datetime.fromisoformat(query['time'].replace('Z', '+00:00'))
            hour = timestamp.strftime('%H:00')
            client = query.get('client', 'unknown')

            # Track hourly distribution
            temporal_analysis['hourly_distribution'][hour] += 1

            # Track query types over time
            qtype = query['question']['type']
            temporal_analysis['query_types_over_time'][hour][qtype] += 1

            # Track blocking effectiveness over time
            temporal_analysis['blocked_ratio_over_time'][hour]['total'] += 1
            if query.get('reason') in ['FilteredBlackList', 'FilteredBlockedService']:
                temporal_analysis['blocked_ratio_over_time'][hour]['blocked'] += 1

            # Track when clients are active
            temporal_analysis['client_activity_hours'][client].add(hour)

        return temporal_analysis

    def analyze_client_behavior(self, queries: list) -> dict:
        """Analyze detailed client behavior patterns"""
        client_analysis = defaultdict(lambda: {
            'total_queries': 0,
            'blocked_queries': 0,
            'unique_domains': set(),
            'query_types': defaultdict(int),
            'active_hours': set(),
            'common_domains': defaultdict(int),
            'protocols': defaultdict(int)  # Added to track DNS protocols used
        })

        for query in queries:
            client = query.get('client', 'unknown')
            timestamp = datetime.fromisoformat(query['time'].replace('Z', '+00:00'))
            domain = query['question']['name']

            analysis = client_analysis[client]
            analysis['total_queries'] += 1
            analysis['unique_domains'].add(domain)
            analysis['query_types'][query['question']['type']] += 1
            analysis['active_hours'].add(timestamp.strftime('%H'))
            analysis['common_domains'][domain] += 1
            analysis['protocols'][query.get('client_proto', 'unknown')] += 1

            if query.get('reason') in ['FilteredBlackList', 'FilteredBlockedService']:
                analysis['blocked_queries'] += 1

        return client_analysis

    def analyze_domain_patterns(self, queries: list) -> dict:
        """Analyze domain access patterns over time"""
        domain_analysis = {
            'trending_domains': defaultdict(lambda: defaultdict(int)),
            'blocked_domains': defaultdict(int),
            'client_domain_mapping': defaultdict(lambda: defaultdict(int)),
            'recurring_patterns': defaultdict(list),
            'response_status': defaultdict(int)  # Added to track DNS response status
        }

        for query in queries:
            timestamp = datetime.fromisoformat(query['time'].replace('Z', '+00:00'))
            hour = timestamp.strftime('%H:00')
            domain = query['question']['name']
            client = query.get('client', 'unknown')

            # Track domain popularity by hour
            domain_analysis['trending_domains'][hour][domain] += 1

            # Track blocked domains and reasons
            if query.get('reason') in ['FilteredBlackList', 'FilteredBlockedService']:
                domain_analysis['blocked_domains'][domain] += 1

            # Track which clients access which domains
            domain_analysis['client_domain_mapping'][client][domain] += 1

            # Track DNS response status
            domain_analysis['response_status'][query.get('status', 'unknown')] += 1

            # Look for recurring patterns
            domain_analysis['recurring_patterns'][domain].append(timestamp)

        return domain_analysis

    # Create visualization for logs data
    def visualize_temporal_patterns(self, temporal_analysis: dict):
        """Create visualizations for temporal patterns"""
        print(f"Creating temporal visualizations for {self.name}...")

        plt.style.use('default')
        fig = plt.figure(figsize=(20, 15))

        # 1. Hourly Query Distribution
        plt.subplot(2, 2, 1)
        hours = sorted(temporal_analysis['hourly_distribution'].keys())
        queries = [temporal_analysis['hourly_distribution'][h] for h in hours]
        plt.plot(hours, queries, marker='o')
        plt.title('Query Distribution by Hour')
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Queries')
        plt.xticks(rotation=45)
        plt.grid(True)

        # 2. Query Types Distribution
        plt.subplot(2, 2, 2)
        query_types = defaultdict(int)
        for hour_data in temporal_analysis['query_types_over_time'].values():
            for qtype, count in hour_data.items():
                query_types[qtype] += count

        types = list(query_types.keys())
        counts = list(query_types.values())
        plt.bar(types, counts)
        plt.title('Query Types Distribution')
        plt.xlabel('Query Type')
        plt.ylabel('Number of Queries')
        plt.xticks(rotation=45)

        # 3. Blocking Rate Over Time
        plt.subplot(2, 2, 3)
        hours = sorted(temporal_analysis['blocked_ratio_over_time'].keys())
        block_rates = []
        for hour in hours:
            data = temporal_analysis['blocked_ratio_over_time'][hour]
            rate = (data['blocked'] / data['total'] * 100) if data['total'] > 0 else 0
            block_rates.append(rate)

        plt.plot(hours, block_rates, marker='o', color='red')
        plt.title('Blocking Rate Over Time')
        plt.xlabel('Hour')
        plt.ylabel('Blocking Rate (%)')
        plt.xticks(rotation=45)
        plt.grid(True)

        # 4. Client Activity
        plt.subplot(2, 2, 4)
        client_activity = defaultdict(int)
        for client, hours in temporal_analysis['client_activity_hours'].items():
            client_activity[client] = len(hours)

        clients = list(client_activity.keys())
        activity = list(client_activity.values())
        plt.bar(clients, activity)
        plt.title('Client Activity (Active Hours)')
        plt.xlabel('Client')
        plt.ylabel('Number of Active Hours')
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.savefig(f"{self.plots_dir}/{self.name}_temporal_analysis.png")
        plt.close()

    # Generate report for logs data
    def generate_insights_report(self, time_span: int):
        """Generate comprehensive insights report"""
        queries = self.logs_data

        temporal_analysis = self.analyze_temporal_patterns(queries['data'])
        client_analysis = self.analyze_client_behavior(queries['data'])
        domain_analysis = self.analyze_domain_patterns(queries['data'])

        # Generate insights
        insights = []

        # Peak Usage Patterns
        peak_hour = max(temporal_analysis['hourly_distribution'].items(),
                       key=lambda x: x[1])[0]
        insights.append(f"Peak DNS query activity occurs at {peak_hour}")

        # Client Behavior Insights
        for client, analysis in client_analysis.items():
            block_rate = (analysis['blocked_queries'] / analysis['total_queries']) * 100
            if block_rate > 20:  # Arbitrary threshold
                insights.append(
                    f"High blocking rate ({block_rate:.1f}%) for client {client}"
                )

            if len(analysis['active_hours']) > 20:  # Active more than 20 hours
                insights.append(
                    f"Client {client} shows unusual activity patterns (active {len(analysis['active_hours'])} hours)"
                )

        # Domain Pattern Insights
        for domain, timestamps in domain_analysis['recurring_patterns'].items():
            if len(timestamps) > 1000:  # High frequency domain
                insights.append(
                    f"High frequency queries to {domain} ({len(timestamps)} queries)"
                )

        return insights

    # Generate stats report
    def generate_stats_html_report(self):
        """Generate an HTML report with analysis and images"""
        stats = self.stats_data
        blocking_rate = (stats['num_blocked_filtering'] / stats['num_dns_queries'] * 100) if stats['num_dns_queries'] > 0 else 0

        html_content = f"""
        <html>
        <head>
            <title>AdGuard Home Analysis - {self.name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .container {{ max-width: 1200px; margin: auto; }}
                .image-container {{ margin: 20px 0; }}
                img {{ max-width: 100%; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .stats-card {{
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 10px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>AdGuard Home Analysis Report - {self.name}</h1>

                <div class="stats-card">
                    <h2>Overview</h2>
                    <p>Total DNS Queries: {stats['num_dns_queries']:,}</p>
                    <p>Blocked Queries: {stats['num_blocked_filtering']:,}</p>
                    <p>Blocking Rate: {blocking_rate:.1f}%</p>
                </div>

                <div class="image-container">
                    <img src="{self.plots_dir}/{self.name}_stats_analysis.png" alt="Analysis Visualizations">
                </div>

                <h2>Top Queried Domains</h2>
                <table>
                    <tr>
                        <th>Domain</th>
                        <th>Query Count</th>
                    </tr>
        """

        # Add top queried domains to the table
        for entry in stats['top_queried_domains'][:10]:  # Get first 10 entries
            domain = list(entry.keys())[0]
            count = list(entry.values())[0]
            html_content += f"""
                <tr>
                    <td>{domain}</td>
                    <td>{count:,}</td>
                </tr>
            """

        html_content += """
                </table>
            </div>
        </body>
        </html>
        """

        with open(f"{self.reports_dir}/{self.name}_stats_report.html", 'w') as f:
            f.write(html_content)

    # Generate logs report
    def generate_logs_html_report(self, temporal_analysis, client_analysis,
                                    domain_analysis, insights, time_span):
        """Generate comprehensive HTML report with all analyses"""
        html_content = f"""
        <html>
        <head>
            <title>Comprehensive DNS Analysis - {self.name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .container {{ max-width: 1200px; margin: auto; }}
                .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                .insight {{ background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 3px; }}
                img {{ max-width: 100%; }}
                table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>DNS Analysis Report - {self.name}</h1>
                <p>Analysis period: Last {time_span} hours</p>

                <div class="section">
                    <h2>Key Insights</h2>
                    {''.join(f'<div class="insight">{insight}</div>' for insight in insights)}
                </div>

                <div class="section">
                    <h2>Temporal Analysis</h2>
                    <img src="{self.plots_dir}/{self.name}_temporal_analysis.png" alt="Temporal Analysis">
                </div>

                <div class="section">
                    <h2>Client Analysis</h2>
                    <table>
                        <tr>
                            <th>Client</th>
                            <th>Total Queries</th>
                            <th>Blocked Queries</th>
                            <th>Blocking Rate</th>
                            <th>Unique Domains</th>
                            <th>Active Hours</th>
                        </tr>
        """

        # Add client analysis data
        for client, data in client_analysis.items():
            block_rate = (data['blocked_queries'] / data['total_queries'] * 100) if data['total_queries'] > 0 else 0
            html_content += f"""
                        <tr>
                            <td>{client}</td>
                            <td>{data['total_queries']:,}</td>
                            <td>{data['blocked_queries']:,}</td>
                            <td>{block_rate:.1f}%</td>
                            <td>{len(data['unique_domains']):,}</td>
                            <td>{len(data['active_hours'])}</td>
                        </tr>
            """

        html_content += """
                    </table>
                </div>
            </div>
        </body>
        </html>
        """

        with open(f"{self.reports_dir}/{self.name}_comprehensive_report.html", 'w') as f:
            f.write(html_content)
