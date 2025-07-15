from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/firewall/override', methods=['POST'])
def firewall_override():
    # Initialize result flags
    success = True
    logs = []
    
    referer = request.headers.get('Referer', '')
    if '192.168.100' not in referer:
        success = False
        logs.append("Security alert: Non-local connection detected. We only allow connections from our local 192.168.100.0/24 network")
    else:
        logs.append("Local connection verified")
        
        user_agent = request.headers.get('User-Agent', '').lower()
        if 'gridsecuritybrowser' not in user_agent:
            success = False
            logs.append("Not utilizing GridSecurityBrowser")
        else:
            logs.append("Admin client verified")
        
            grid_protocol = request.headers.get('Accept-Language', '').lower()
            if 'pt-br' not in grid_protocol:
                success = False
                if 'pt-pt' in grid_protocol:
                    logs.append("Security alert: NO, no that portuguese, the better one!")
                else:
                    logs.append("Security alert: Wait, the grid security only talks in Portuguese!")
            else:
                logs.append("Grid protocol version verified")
    
    # All checks complete - determine if ALL checks passed
    if success:
        # User has passed ALL security checks, definitely grant the flag
        logs.append("All security checks passed successfully!")
        return jsonify({
            "message": "dalctf{sp00f3d_gr1d_n0d3}",
            "log": "FULL ACCESS GRANTED: Master firewall node unlocked"
        })
    else:
        # At least one check failed, deny access
        return jsonify({
            "message": "Access Denied: Security checks failed",
            "log": " | ".join(logs)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
