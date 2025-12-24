# Main application
from auth import LoginSystem
from qr_code import QRGenerator
from flask import Flask, jsonify, request
import webbrowser
import threading
import time

app = Flask(__name__)

# Create system objects
login_system = LoginSystem()
qr_system = QRGenerator()
current_user = None

# HTML page (your existing HTML code here)
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>QR ID System</title>
    <style>
        body { font-family: Arial; padding: 20px; max-width: 600px; margin: auto; }
        .box { background: #f0f8ff; padding: 20px; margin: 20px 0; border-radius: 10px; }
        input, button { padding: 10px; margin: 5px; width: 95%; }
        button { background: #4CAF50; color: white; border: none; cursor: pointer; }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>🎫 QR ID Card System</h1>
    
    <div class="box">
        <h3>🔐 Login</h3>
        <input id="email" placeholder="Email" value="admin@school.com">
        <input id="password" type="password" placeholder="Password" value="Admin@123">
        <button onclick="login()">Login</button>
        <div id="loginResult"></div>
    </div>
    
    <div class="box">
        <h3>📱 Generate QR Code</h3>
        <button onclick="generateQR()">Generate My QR</button>
        <div id="qrResult"></div>
    </div>
    
    <div class="box">
        <h3>🔍 Scan QR Code</h3>
        <input id="scanInput" placeholder="Paste QR code here">
        <button onclick="scanQR()">Scan QR</button>
        <div id="scanResult"></div>
    </div>
    
    <script>
        async function login() {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email, password})
            });
            
            const result = await response.json();
            const div = document.getElementById('loginResult');
            
            if(result.success) {
                div.innerHTML = `<p class="success">✅ Welcome ${result.user.name}!</p>`;
            } else {
                div.innerHTML = `<p class="error">❌ ${result.message}</p>`;
            }
        }
        
        async function generateQR() {
            const response = await fetch('/api/generate_qr');
            const result = await response.json();
            const div = document.getElementById('qrResult');
            
            if(result.success) {
                div.innerHTML = `<p class="success">✅ QR Code: ${result.qr_data}</p>`;
            } else {
                div.innerHTML = `<p class="error">❌ ${result.message}</p>`;
            }
        }
        
        async function scanQR() {
            const qrData = document.getElementById('scanInput').value;
            
            const response = await fetch('/api/scan_qr', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({qr_data: qrData})
            });
            
            const result = await response.json();
            const div = document.getElementById('scanResult');
            
            if(result.success) {
                div.innerHTML = `<p class="success">✅ Scanned: ${result.user_info.name} (${result.user_info.role})</p>`;
            } else {
                div.innerHTML = `<p class="error">❌ ${result.message}</p>`;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML

@app.route('/api/login', methods=['POST'])
def api_login():
    global current_user
    data = request.json
    result = login_system.login(data.get('email'), data.get('password'))
    if result["success"]:
        current_user = result["user"]
    return jsonify(result)

@app.route('/api/generate_qr', methods=['GET'])
def api_generate_qr():
    global current_user
    if current_user:
        qr_data = qr_system.generate_qr(current_user)
        return jsonify({
            "success": True,
            "qr_data": qr_data,
            "user": current_user
        })
    return jsonify({"success": False, "message": "Please login first"})

@app.route('/api/scan_qr', methods=['POST'])
def api_scan_qr():
    data = request.json
    qr_input = data.get('qr_data')
    
    if qr_input:
        user_info = qr_system.scan_qr(qr_input)
        if user_info:
            return jsonify({"success": True, "user_info": user_info})
    return jsonify({"success": False, "message": "Invalid QR code"})

if __name__ == "__main__":
    print("=" * 50)
    print("🎫 QR ID Card System")
    print("=" * 50)
    
    # Function to open browser
    def open_browser():
        time.sleep(2)  # Wait for server to start
        webbrowser.open("http://localhost:5000")
        print("✅ Browser opened!")
    
    # Start browser thread
    threading.Thread(target=open_browser).start()
    
    print("🌐 Opening browser automatically...")
    print("   URL: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, port=5000)