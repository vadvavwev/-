from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from utils.exceptions import register_error_handlers
from middleware.logging_middleware import setup_logging, register_logging_middleware


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Database
    db.init_app(app)

    # CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Logging
    import os
    os.makedirs("logs", exist_ok=True)
    setup_logging(app)
    register_logging_middleware(app)

    # Error handlers
    register_error_handlers(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.employees import employees_bp
    from routes.categories import categories_bp
    from routes.devices import devices_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(devices_bp)

    # Health check endpoint
    @app.route("/api/health")
    def health_check():
        return {"status": "healthy"}

    # Create tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
