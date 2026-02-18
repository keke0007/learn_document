from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'message': 'Hello from Docker!',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/info')
def info():
    return jsonify({
        'hostname': os.getenv('HOSTNAME', 'unknown'),
        'python_version': os.sys.version
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
