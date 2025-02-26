import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create a minimal app for database operations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models to include them in migrations
# We're importing here to avoid circular dependencies
# Note: models.py in the project root will import db from this file
from models import User, Post, Comment, Category, Tag

if __name__ == '__main__':
    print("Flask-Migrate setup script complete.")
    print("You can now run the following commands:")
    print("flask db init")
    print("flask db migrate -m 'Initial migration'")
    print("flask db upgrade")
