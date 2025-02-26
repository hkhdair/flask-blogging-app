from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse  # Use Python's standard library instead of werkzeug
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, ProfileForm
from app.models import User
import os
import uuid
from flask import current_app

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('blog.index')
        
        flash('Login successful!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('blog.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # Check if username is already taken by another user
        if form.username.data != current_user.username:
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                flash('Username already taken.', 'danger')
                return redirect(url_for('auth.profile'))
        
        # Check if email is already taken by another user
        if form.email.data != current_user.email:
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('Email already registered.', 'danger')
                return redirect(url_for('auth.profile'))
        
        # Handle profile image upload
        if form.profile_image.data:
            # Save the profile image
            filename = str(uuid.uuid4()) + os.path.splitext(form.profile_image.data.filename)[1]
            form.profile_image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            
            # Delete old profile image if it's not the default
            if current_user.profile_image != 'default.jpg':
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.profile_image))
                except:
                    # File might not exist, ignore
                    pass
            
            current_user.profile_image = filename
        
        # Update user information
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        # Pre-populate form with current user data
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    
    # Calculate total views across all user posts
    total_views = sum(post.views for post in current_user.posts)
    
    return render_template('auth/profile.html', title='Profile', form=form, total_views=total_views)
