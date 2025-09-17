from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    with open('config/config.json') as f:
        config = json.load(f)
    return jsonify(config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
