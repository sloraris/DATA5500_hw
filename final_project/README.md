# Final Project - DATA 5500
**Because why query someone else's API when I've got like 8 of them at home?**

## Description
This project is a Python script that queries my self-hosted AdGuard Home DNS server's API to retrieve and analyze DNS query statistics. Sure, AdGuard Home has a web interface, but I wanted to see if I could get the data programmatically and let Python find the patterns. It's good practice, ya know?

## Accessing the API
AdGuard Home API documentation can be found on the [AdGuard Home GitHub repository](https://github.com/AdguardTeam/AdGuardHome/blob/master/openapi/openapi.yaml) in OpenAPI format, which is not super easy to read in raw form (though I did try initially). So, they recommend using [Swagger Editor](https://editor.swagger.io/) to view the API documentation. To do this, I just copied the raw OpenAPI file into the Swagger editor and read it there.

## Methodology
**I used the `Andy Brim API method` for this project:**
1. I got the link to the API
2. I stared at it for a while
3. I identified the data I wanted to retrieve

**I then used the `Classic Developer Method` for the additional steps:**
1. RTFM (Read The Friggin Manual)
2. Profit

## Results
