# Firewall Node Challenge

## Description
Players need to bypass a firewall by manipulating HTTP headers. This challenge focuses on header-based security checks.

## Setup
1. Build and run the Docker container:
```
docker build -t firewall-node .
docker run -p 8080:8080 firewall-node
```

## Solution
To solve this challenge, players need to:

1. Understand that the security is based entirely on HTTP headers
2. Craft a request with the following headers:
   - Referer: http://localhost:8080/ or http://127.0.0.1:8080/
   - User-Agent: (anything containing) GridSecurityAdmin
   - Authorization: Bearer TRON-GRID-(anything)
   - X-Firewall-Key: END-OF-LINE-1982
   - X-Grid-Protocol: CLU/2.0

Example curl command to solve:
```
curl -X POST   -H "Referer: 192.168.100.1" -H "Accept-Language: pt-br"   -H "User-Agent: GridSecurityBrowser"   -H "Content-Type: application/json"   -d '{}' http://localhost:8003/api/firewall/override
```

## Flags
- `dalctf{m4st3r_0f_h34d3rs_4nd_f1r3w4lls}`
