"""
This is a utility script to fix the URL building error in the Flask blog application.

This script adds a new route for search results that accepts a query parameter
from GET requests, which fixes the BuildError related to the search_results endpoint.

To use this script:
1. Run it with Python to see the issues it fixes
2. Apply the changes manually to your application
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

"""
ISSUE: Missing search_results route that accepts query parameter

SOLUTION:

In your app/blog/routes.py file, add a new route:

@bp.route('/search-results')
def search_results():
    query = request.args.get('query', '')
    if not query:
        flash('Please enter a search term', 'warning')
        return redirect(url_for('blog.search'))
        
    page = request.args.get('page', 1, type=int)
    # Search in title, content, and summary
    posts = Post.query.filter(
        Post.published == True,
        or_(
            Post.title.ilike(f'%{query}%'),
            Post.content.ilike(f'%{query}%'),
            Post.summary.ilike(f'%{query}%')
        )
    ).order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
    
    return render_template('blog/search_results.html', 
                          title=f'Search Results for "{query}"', 
                          query=query, posts=posts)
"""

"""
ISSUE: Incorrect action URL in the search form

SOLUTION:

In your app/templates/blog/index.html file, update the search form:

Change:
<form action="{{ url_for('blog.search_results') }}" method="get">

To:
<form action="{{ url_for('blog.search_results') }}" method="get">
    
Or alternatively:
<form action="{{ url_for('blog.search') }}" method="get">
"""

if __name__ == "__main__":
    print("This script contains instructions for fixing the search functionality in the Flask blog app.")
    print("\nTo fix the BuildError, you need to:")
    print("1. Add a new route '/search-results' that accepts a query parameter from GET requests")
    print("2. Update the search form in index.html to point to the correct endpoint")
    print("\nSee the code comments for implementation details.")
