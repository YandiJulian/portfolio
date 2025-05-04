from flask import Flask, render_template, request, jsonify
import subprocess
import ipaddress

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping', methods=['POST'])
def ping():
    ip = request.json.get('ip')
    try:
        result = subprocess.run(['ping', '-n', '1', ip], stdout=subprocess.PIPE)
        success = result.returncode == 0
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/subnet', methods=['POST'])
def subnet():
    ip = request.json.get('ip')
    cidr = request.json.get('cidr')
    try:
        network = ipaddress.ip_network(f"{ip}/{cidr}", strict=False)
        return jsonify({
            'network': str(network.network_address),
            'broadcast': str(network.broadcast_address),
            'netmask': str(network.netmask),
            'hosts': network.num_addresses - 2
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
