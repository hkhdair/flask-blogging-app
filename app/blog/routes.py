from flask import render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import current_user, login_required
from app import db
from app.blog import bp
from app.blog.forms import PostForm, CommentForm, CategoryForm, TagForm, SearchForm
from app.models import Post, Comment, Category, Tag, User
from datetime import datetime
import os
import uuid
from sqlalchemy import or_, func
import markdown

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
    return render_template('blog/index.html', title='Home', posts=posts)

@bp.route('/post/<string:slug>', methods=['GET', 'POST'])
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    # Increment view count
    post.views += 1
    db.session.commit()
    
    # Handle comments
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You need to be logged in to comment.', 'info')
            return redirect(url_for('auth.login', next=request.url))
        
        comment = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('blog.post', slug=post.slug))
    
    # Get comments
    comments = Comment.query.filter_by(post_id=post.id, parent_id=None).order_by(Comment.created_at.desc()).all()
    
    # Convert markdown content to HTML
    post_content_html = markdown.markdown(post.content, extensions=['tables', 'fenced_code'])
    
    return render_template('blog/post.html', title=post.title, post=post, 
                          form=form, comments=comments, post_content_html=post_content_html)

@bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, 
                   content=form.content.data,
                   summary=form.summary.data,
                   author=current_user,
                   published=form.published.data)
        
        # Handle slug
        if form.slug.data:
            post.slug = form.slug.data
        else:
            post.generate_slug()
        
        # Handle category
        if form.category.data != 0:  # 0 is the placeholder "Select Category" option
            category = Category.query.get(form.category.data)
            post.category = category
        
        # Handle featured image
        if form.featured_image.data:
            filename = post.save_featured_image(form.featured_image.data)
            post.featured_image = filename
        
        # Handle tags
        if form.tags.data:
            tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
            for tag_name in tag_names:
                # Check if tag exists, create if not
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name, slug='-'.join(tag_name.lower().split()))
                    db.session.add(tag)
                post.tags.append(tag)
        
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog.post', slug=post.slug))
    
    return render_template('blog/create_post.html', title='New Post', form=form, legend='New Post')

@bp.route('/post/<string:slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    # Check if user is the author or admin
    if post.author != current_user and not current_user.is_admin:
        abort(403)
    
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        
        # Handle slug
        if form.slug.data:
            post.slug = form.slug.data
        
        post.content = form.content.data
        post.summary = form.summary.data
        post.published = form.published.data
        
        # Handle category
        if form.category.data != 0:  # 0 is the placeholder "Select Category" option
            category = Category.query.get(form.category.data)
            post.category = category
        else:
            post.category = None
        
        # Handle featured image
        if form.featured_image.data:
            # Delete old image if it exists
            if post.featured_image:
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], post.featured_image))
                except:
                    pass
            
            # Save new image
            filename = post.save_featured_image(form.featured_image.data)
            post.featured_image = filename
        
        # Handle tags
        post.tags = []  # Remove existing tags
        if form.tags.data:
            tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
            for tag_name in tag_names:
                # Check if tag exists, create if not
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name, slug='-'.join(tag_name.lower().split()))
                    db.session.add(tag)
                post.tags.append(tag)
        
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('blog.post', slug=post.slug))
    elif request.method == 'GET':
        # Pre-populate form with post data
        form.title.data = post.title
        form.slug.data = post.slug
        form.content.data = post.content
        form.summary.data = post.summary
        form.published.data = post.published
        
        if post.category:
            form.category.data = post.category.id
        else:
            form.category.data = 0
        
        form.tags.data = ', '.join([tag.name for tag in post.tags])
    
    return render_template('blog/create_post.html', title='Edit Post', 
                          form=form, legend='Edit Post')

@bp.route('/post/<string:slug>/delete', methods=['POST'])
@login_required
def delete_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    # Check if user is the author or admin
    if post.author != current_user and not current_user.is_admin:
        abort(403)
    
    # Delete featured image if it exists
    if post.featured_image:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], post.featured_image))
        except:
            pass
    
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('blog.index'))

@bp.route('/category/<string:slug>')
def category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category=category, published=True).order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
    return render_template('blog/category.html', title=f'Category: {category.name}', 
                          category=category, posts=posts)

@bp.route('/tag/<string:slug>')
def tag(slug):
    tag = Tag.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = tag.posts.filter_by(published=True).order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
    return render_template('blog/tag.html', title=f'Tag: {tag.name}', 
                          tag=tag, posts=posts)

@bp.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user, published=True).order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
    return render_template('blog/user_posts.html', title=f'Posts by {user.username}', 
                          user=user, posts=posts)

@bp.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('blog.search_results_by_param', query=form.query.data))
    
    return render_template('blog/search.html', title='Search', form=form)

@bp.route('/search/<string:query>')
def search_results_by_param(query):
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

@bp.route('/search_results')
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

# Admin routes for category and tag management
@bp.route('/admin/categories', methods=['GET', 'POST'])
@login_required
def manage_categories():
    # Only admins can manage categories
    if not current_user.is_admin:
        abort(403)
    
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, 
                          description=form.description.data)
        
        # Handle slug
        if form.slug.data:
            category.slug = form.slug.data
        else:
            category.slug = '-'.join(form.name.data.lower().split())
        
        db.session.add(category)
        db.session.commit()
        flash('Category has been created!', 'success')
        return redirect(url_for('blog.manage_categories'))
    
    categories = Category.query.order_by(Category.name).all()
    return render_template('blog/manage_categories.html', 
                          title='Manage Categories', 
                          form=form, categories=categories)

@bp.route('/admin/category/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    # Only admins can edit categories
    if not current_user.is_admin:
        abort(403)
    
    category = Category.query.get_or_404(id)
    form = CategoryForm()
    
    if form.validate_on_submit():
        category.name = form.name.data
        
        # Handle slug
        if form.slug.data:
            category.slug = form.slug.data
        else:
            category.slug = '-'.join(form.name.data.lower().split())
        
        category.description = form.description.data
        
        db.session.commit()
        flash('Category has been updated!', 'success')
        return redirect(url_for('blog.manage_categories'))
    elif request.method == 'GET':
        # Pre-populate form with category data
        form.name.data = category.name
        form.slug.data = category.slug
        form.description.data = category.description
    
    return render_template('blog/edit_category.html', 
                          title='Edit Category', 
                          form=form, category=category)

@bp.route('/admin/category/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    # Only admins can delete categories
    if not current_user.is_admin:
        abort(403)
    
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Category has been deleted!', 'success')
    return redirect(url_for('blog.manage_categories'))

@bp.route('/admin/tags', methods=['GET', 'POST'])
@login_required
def manage_tags():
    # Only admins can manage tags
    if not current_user.is_admin:
        abort(403)
    
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data)
        
        # Handle slug
        if form.slug.data:
            tag.slug = form.slug.data
        else:
            tag.slug = '-'.join(form.name.data.lower().split())
        
        db.session.add(tag)
        db.session.commit()
        flash('Tag has been created!', 'success')
        return redirect(url_for('blog.manage_tags'))
    
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('blog/manage_tags.html', 
                          title='Manage Tags', 
                          form=form, tags=tags)

@bp.route('/admin/tag/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tag(id):
    # Only admins can edit tags
    if not current_user.is_admin:
        abort(403)
    
    tag = Tag.query.get_or_404(id)
    form = TagForm()
    
    if form.validate_on_submit():
        tag.name = form.name.data
        
        # Handle slug
        if form.slug.data:
            tag.slug = form.slug.data
        else:
            tag.slug = '-'.join(form.name.data.lower().split())
        
        db.session.commit()
        flash('Tag has been updated!', 'success')
        return redirect(url_for('blog.manage_tags'))
    elif request.method == 'GET':
        # Pre-populate form with tag data
        form.name.data = tag.name
        form.slug.data = tag.slug
    
    return render_template('blog/edit_tag.html', 
                          title='Edit Tag', 
                          form=form, tag=tag)

@bp.route('/admin/tag/<int:id>/delete', methods=['POST'])
@login_required
def delete_tag(id):
    # Only admins can delete tags
    if not current_user.is_admin:
        abort(403)
    
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag has been deleted!', 'success')
    return redirect(url_for('blog.manage_tags'))

@bp.route('/categories-sidebar')
def categories_sidebar():
    """Endpoint for HTMX to load categories in the sidebar"""
    categories = Category.query.order_by(Category.name).all()
    return render_template('blog/partials/categories_sidebar.html', categories=categories)

@bp.route('/tags-sidebar')
def tags_sidebar():
    """Endpoint for HTMX to load tags in the sidebar"""
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('blog/partials/tags_sidebar.html', tags=tags)
