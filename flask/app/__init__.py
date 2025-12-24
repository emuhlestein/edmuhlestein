from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change-me-to-something-strong'

    @app.route("/")
    def home():
        return "<h1>Welcome to edmuhlestein.com</h1><p>Flask + FastAPI + Nginx + Certbot deployed!</p><br>FastAPI available through /api/hello or /api/health"

    @app.route("/health")
    def health():
        return "OK", 200

    return app
