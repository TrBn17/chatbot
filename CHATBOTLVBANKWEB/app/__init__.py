from flask import Flask
from .chat_routes import user_bp
from .chromadb_routes import chromadb_bp
def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp, url_prefix="/api/chat")
    app.register_blueprint(chromadb_bp, url_prefix="/api/chromadb")
    return app
