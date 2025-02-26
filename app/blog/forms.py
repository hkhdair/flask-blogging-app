from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Optional
from app.models import Category, Tag

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=100)])
    slug = StringField('Slug (URL)', validators=[Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    summary = TextAreaField('Summary', validators=[Length(max=200)])
    category = SelectField('Category', coerce=int, validators=[Optional()])
    tags = StringField('Tags (comma separated)', validators=[Optional()])
    featured_image = FileField('Featured Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    published = BooleanField('Published', default=True)
    submit = SubmitField('Save Post')
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(0, '-- Select Category --')] + [(c.id, c.name) for c in Category.query.order_by('name').all()]

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired(), Length(min=3, max=1000)])
    submit = SubmitField('Post Comment')

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=50)])
    slug = StringField('Slug (URL)', validators=[Length(max=50)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Save Category')

class TagForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=50)])
    slug = StringField('Slug (URL)', validators=[Length(max=50)])
    submit = SubmitField('Save Tag')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
