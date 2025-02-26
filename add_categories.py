"""
Script to add initial categories to the blog database.
This script can be run directly in the Flask shell:

1. Start the Flask shell:
   flask shell

2. In the shell, run:
   from add_categories import add_categories
   add_categories()
"""

from app.models import Category
from app import db

# List of categories with name, slug, and description
categories = [
    {
        'name': 'Technology',
        'slug': 'technology',
        'description': 'Posts about the latest in technology, programming languages, frameworks, and tools.'
    },
    {
        'name': 'Web Development',
        'slug': 'web-development',
        'description': 'Articles about web development, HTML, CSS, JavaScript, and modern web frameworks.'
    },
    {
        'name': 'Data Science',
        'slug': 'data-science',
        'description': 'Explorations of data analysis, machine learning, artificial intelligence, and statistics.'
    },
    {
        'name': 'Python',
        'slug': 'python',
        'description': 'Everything related to Python programming language, libraries, and frameworks like Flask and Django.'
    },
    {
        'name': 'DevOps',
        'slug': 'devops',
        'description': 'Content about CI/CD, containerization, cloud services, and infrastructure as code.'
    },
    {
        'name': 'Career',
        'slug': 'career',
        'description': 'Tips and advice for career development in the tech industry.'
    },
    {
        'name': 'Tutorials',
        'slug': 'tutorials',
        'description': 'Step-by-step guides and how-to tutorials on various programming topics.'
    },
    {
        'name': 'Opinion',
        'slug': 'opinion',
        'description': 'Personal thoughts and perspectives on technology trends and developments.'
    }
]

def add_categories():
    # Check if categories already exist
    existing_categories = Category.query.all()
    if existing_categories:
        print(f"Found {len(existing_categories)} existing categories. Here they are:")
        for category in existing_categories:
            print(f" - {category.name}")
        print("\nNo new categories were added to avoid duplicates.")
    else:
        # Add categories to the database
        for category_data in categories:
            category = Category(
                name=category_data['name'],
                slug=category_data['slug'],
                description=category_data['description']
            )
            db.session.add(category)
        
        # Commit the changes
        db.session.commit()
        print(f"Added {len(categories)} categories to the database:")
        for category in categories:
            print(f" - {category['name']}")

    print("\nDone!")
