import requests
from flask import Flask, jsonify, render_template

FASTAPI_URL = "http://fastapi:8000"   # Docker network service name


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change-me-to-something-strong'

    @app.route("/")
    def home():
        return render_template('index.html')   # Renders templates/index.html

    @app.route("/health")
    def health():
        return "OK", 200
    
    @app.route("/proxy/hello")
    def proxy_hello():
        try:
            response = requests.get(f"{FASTAPI_URL}/hello")
            response.raise_for_status()
            data = response.json()
            return jsonify({"from_fastapi": data})
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/proxy/health")
    def proxy_health():
        try:
            response = requests.get(f"{FASTAPI_URL}/health")
            return jsonify({"fastapi_status": response.json()})
        except requests.exceptions.RequestException:
            return jsonify({"fastapi_status": "down"}), 503

    return app
