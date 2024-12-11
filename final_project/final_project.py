from adguard import *

# Main
if __name__ == "__main__":
    # Load config
    servers = read_config("secrets.yaml")
    output_dir = "data"

    # Analyze all servers in config
    server_instances = {}
    for server in servers:
        server_name = server['name']
        server_instances[server_name] = AdGuardAnalyzer(server, output_dir)


