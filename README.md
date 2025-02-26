# FlaskBlog

A modern blogging application built with Flask and modern web technologies. This application provides a complete blogging platform with user management, content organization, and a responsive design.

## Features

- User authentication and authorization
- Create, read, update, and delete blog posts
- Rich text editing with Markdown support
- Responsive design with Bootstrap 5
- Comment system with threading support
- Tags and categories for content organization
- Search functionality
- User profiles with profile pictures
- View count tracking for posts
- Admin dashboard for site management

## Technology Stack

- **Backend**: Flask
- **Database**: SQLite (can be easily replaced with PostgreSQL for production)
- **Frontend**:
  - HTML5, CSS3, JavaScript (ES6+)
  - Bootstrap 5 for responsive design
  - HTMX for dynamic content without writing JavaScript
  - Alpine.js for lightweight interactivity
  - Font Awesome for icons
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Database ORM**: SQLAlchemy
- **Markdown Support**: Markdown
- **Security**: CSRF protection, password hashing

## Installation and Setup

1. Clone the repository
   ```
   git clone <repository-url>
   cd flaskblog
   ```

2. Set up a virtual environment
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Unix/MacOS
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. Run the application
   ```
   flask run
   ```

6. Access the application at http://127.0.0.1:5000

## Creating an Admin User

1. Start the Flask shell
   ```
   flask shell
   ```

2. Create an admin user
   ```python
   from app import db
   from app.models import User
   
   admin = User(username='admin', email='admin@example.com', is_admin=True)
   admin.set_password('your-secure-password')
   db.session.add(admin)
   db.session.commit()
   ```

## Project Structure

The application follows a modular blueprint structure:

- `app/`: Main application package
  - `__init__.py`: Application factory
  - `models.py`: Database models
  - `auth/`: Authentication blueprint
    - `routes.py`: Authentication routes
    - `forms.py`: Authentication forms
  - `blog/`: Blog functionality blueprint
    - `routes.py`: Blog routes
    - `forms.py`: Blog forms
  - `static/`: Static files (CSS, JS, images)
    - `css/`: CSS files
    - `js/`: JavaScript files
    - `profile_pics/`: User profile images
    - `post_images/`: Post featured images
  - `templates/`: Jinja2 templates
    - `auth/`: Authentication templates
    - `blog/`: Blog templates
    - `errors/`: Error pages
- `config.py`: Configuration settings
- `migrations/`: Database migrations
- `requirements.txt`: Project dependencies
- `run.py`: Application entry point

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation
- SQLAlchemy documentation
- Bootstrap 5 documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
