"""
Add this code to the end of your routes.py file to fix the search results route.
"""

@bp.route('/search-results')  # This won't work because Flask converts hyphens to underscores
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
