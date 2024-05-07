from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from .models import db, login_manager


socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///tictactoe.sqlite"

    )
    CORS(app)

    # init db and create tables
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints
    from .login import login_bp
    app.register_blueprint(login_bp)
    
    
    from .register import register_bp
    app.register_blueprint(register_bp)

    
    from .lobby import lobby_bp
    app.register_blueprint(lobby_bp)


    from tictactoe_backend.game import game_bp
    app.register_blueprint(game_bp)
    

    from tictactoe_backend.profile import profile_bp
    app.register_blueprint(profile_bp)
    

    login_manager.init_app(app)
    socketio.init_app(app)

    return app

if __name__ == "__main__": create_app()