#!/usr/bin/env python3
import hashlib
import hmac
import binascii
import subprocess
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session

# --- Challenge Configuration ---
MASTER_KEY = b'REDACTED' # This is not the actual master key, if redacted it
SAMPLE_COMMAND = 'echo "testing"'

app = Flask(__name__)
app.secret_key = os.urandom(24)

def calculate_mac(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(MASTER_KEY + data).hexdigest()

@app.route('/')
def index():
    sample_command = SAMPLE_COMMAND
    sample_mac = calculate_mac(sample_command)
    key_length = len(MASTER_KEY)
    
    return render_template('index.html', 
                           sample_command=sample_command, 
                           sample_mac=sample_mac, 
                           key_length=key_length)

@app.route('/execute', methods=['POST'])
def execute():
    if 'file' not in request.files or 'signature' not in request.form:
        flash('Missing required file or signature', 'error')
        return redirect(url_for('index'))
    
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file_content_bytes = uploaded_file.read()
    signature = request.form['signature']
    
    expected_mac = calculate_mac(file_content_bytes.strip())
    
    if not hmac.compare_digest(signature, expected_mac):
        flash('Invalid signature! Access denied.', 'error')
        return redirect(url_for('index'))
    
    print("Signature is valid, proceeding to decode and execute the command.")

    file_content_str = file_content_bytes.decode('latin-1').strip()
    # Remove null bytes if they exist
    file_content_str = file_content_str.replace('\x00', '')
    
    print(f"Results string {file_content_str}")
    
    # Execute the file content if signature is valid
    try:
        result = subprocess.check_output(file_content_str, shell=True, stderr=subprocess.STDOUT, text=True)
        return render_template('result.html', 
                              execution_result=result, 
                              status="Command executed successfully")
    except subprocess.CalledProcessError as e:
        return render_template('result.html', 
                              execution_result=e.output, 
                              status="Command execution failed")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, debug=False)
