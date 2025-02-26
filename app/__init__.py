from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import config
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # Set up login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.blog import bp as blog_bp
    app.register_blueprint(blog_bp)
    
    # Create a handler for 404 errors
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    # Create a handler for 500 errors
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Add context processor for template variables
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    # Import error templates
    from flask import render_template
    
    # Create uploads directory if it doesn't exist
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register CLI commands
    register_commands(app)
    
    return app

def register_commands(app):
    """Register Click commands."""
    @app.cli.command("create-admin")
    def create_admin():
        """Create an admin user."""
        from app.models import User
        from flask import current_app
        
        username = input("Admin username: ")
        email = input("Admin email: ")
        password = input("Admin password: ")
        
        user = User(username=username, email=email, is_admin=True)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        print(f"Admin user {username} created!")
