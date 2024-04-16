from flask import Flask, flash, render_template, request, redirect, url_for, jsonify, abort, Response
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length
from wtforms.validators import Email
from flask_migrate import Migrate
from wtforms.validators import InputRequired, Length, Email 
from flask_mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
import re
# import shutil
from datetime import datetime
from flask_migrate import Migrate
# from flask_orm import ORM
# from flask import app_ctx
# from .extension import SQLAlchemy
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import declarative_base
# from flask_sqlalchemy import SQLAlchemy

# ...



app = Flask(__name__, static_url_path='/static')
basedir = os.path.abspath(os.path.dirname((__file__)))
database = "app.db"
con = sqlite3.connect(os.path.join(basedir, database))
mail = Mail(app)
# orm = ORM(app, database)

# db = SQLAlchemy(model_class=declarative_base())
app.config['SECRET_KEY'] = "jhkxhiuydu"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['MAIL_SERVER'] = 'intexcoin.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'info@intexcoin.com'
app.config['MAIL_SERVER'] = 'server148.web-hosting.com'
#app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder for uploaded files
# app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static/uploads')  # Folder for uploaded files
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed file extensions
# Assuming your app variable is named 'app'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.add_url_rule('/uploads/<filename>', 'uploads', build_only=True)









# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True,  nullable=False)
    email = db.Column(db.String(255), unique=True , nullable=False)
    password = db.Column(db.String(255) , nullable=False)

    def check_password(self, password):
        check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def create(self, username='', email='', password=''):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def commit(self):
        db.session.commit()

class Blog(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable=False)
    sub_title = db.Column(db.String(255) , nullable=False)
    contentone = db.Column(db.String(500) , nullable=False)
    contenttwo = db.Column(db.String(500) , nullable=False)
    contentthree = db.Column(db.String(500) , nullable=False)
    content = db.Column(db.String(500))
    main_image = db.Column(db.LargeBinary)
    main_image_filename = db.Column(db.String(100))
    main_image_one = db.Column(db.LargeBinary)
    main_image_one_filename = db.Column(db.String(100))
    main_image_two = db.Column(db.LargeBinary)
    main_image_two_filename = db.Column(db.String(100))
    comments = db.relationship('Comment', back_populates='blog')
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Events(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    main_image = db.Column(db.LargeBinary)
    main_image_filename=db.Column(db.String(100))
    content = db.Column(db.String(500))

class Jobs(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    main_image = db.Column(db.LargeBinary)
    main_image_filename= db.Column(db.String(100))   
    content = db.Column(db.String(500))
class Gallery(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    main_image = db.Column(db.LargeBinary)
    description= db.Column(db.String(255))

class Publication(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    main_image = db.Column(db.LargeBinary)
    main_image_filename=db.Column(db.String(100))
    content = db.Column(db.String(500))





from datetime import datetime
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    blog = db.relationship('Blog', back_populates='comments')

class CommentForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    content = TextAreaField('Comment', validators=[InputRequired(), Length(min=1, max=500)])
    submit_comment = SubmitField('Add Comment')

class RegistrationForm(FlaskForm):
    name = StringField('name', validators=[])
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    submit = SubmitField('Log In')
    

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    submit = SubmitField('Sign Up')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST' and form.validate():
        # Check if the username already exists
        existing_username = Users.query.filter_by(username=form.username.data).first()
        if existing_username:
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('signup.html', form=form)

        # Check if the email already exists
        existing_email = Users.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email address already in use. Please use a different one.', 'error')
            return render_template('signup.html', form=form)

        # If username and email are unique, proceed with account creation
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha1', salt_length=8)
        new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate():
        user = Users.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))  # Replace 'dashboard' with the route you want to redirect to after login

        flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('blog_list'))  # Replace 'home' with the route you want to redirect to after logout

@app.route('/createblog', methods=['GET', 'POST'])
@login_required
def Admincreateblog():
    if request.method == 'POST':
        title = request.form['title']
        sub_title = request.form['sub_title']
        content = request.form['content']
        contentone = request.form['contentone']
        contenttwo = request.form['contenttwo']
        contentthree = request.form['contentthree']

         # Ensure the UPLOAD_FOLDER exists
        upload_folder = os.path.join(app.static_folder, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        print("UPLOAD_FOLDER:", upload_folder)  # Debugging line
        # Upload Main Image
        main_image = request.files['main_image']
        if main_image and allowed_file(main_image.filename):
            filename = secure_filename(main_image.filename)
            print("Saving to:", os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Debugging line
            main_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main_image_filename = filename
        else:
            main_image_filename = None

        # Upload Image One
        main_image_one = request.files['main_image_one']
        if main_image_one and allowed_file(main_image_one.filename):
            filename = secure_filename(main_image_one.filename)
            main_image_one.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main_image_one_filename = filename
        else:
            main_image_one_filename = None

        # Upload Image Two
        main_image_two = request.files['main_image_two']
        if main_image_two and allowed_file(main_image_two.filename):
            filename = secure_filename(main_image_two.filename)
            main_image_two.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main_image_two_filename = filename
        else:
            main_image_two_filename = None

        
        
        
        
        
        
        
        new_post = Blog(
            title=title,
            sub_title=sub_title,
            content=content,
            contentone = contentone,
            contenttwo = contenttwo,
            contentthree = contentthree,
            main_image_filename=main_image_filename,
            main_image_one_filename=main_image_one_filename,
            main_image_two_filename=main_image_two_filename
        )

        db.session.add(new_post)
        db.session.commit()
        flash('Post has be made')

        return redirect(url_for('Admincreateblog'))

    return render_template('createblog.html')
       
@app.route('/blog')
def blog_list():
    blogs = Blog.query.all()
    return render_template('blog_list.html', blogs=blogs)
 
 
@app.route('/blog/<int:blog_id>', methods=['GET', 'POST'])
def view_blog(blog_id):
    blog = Blog.query.get(blog_id)
    blogs = Blog.query.all()

    if not blog:
        abort(404)

    comments = Comment.query.filter_by(blog_id=blog.id).order_by(Comment.timestamp.desc()).all()

    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        email = comment_form.email.data
        content = comment_form.content.data

        new_comment = Comment(email=email, content=content, blog_id=blog.id)
        db.session.add(new_comment)
        db.session.commit()

        flash('Comment added successfully!', 'success')

        # Redirect to the same blog post after submitting the comment
        return redirect(url_for('view_blog', blog_id=blog.id))

    return render_template('view_blog.html', blog=blog, comments=comments, comment_form=comment_form, blogs = blogs)

@app.route('/updateblog/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def update_blog(blog_id):
    blog = Blog.query.get(blog_id)

    if not blog:
        abort(404)

    if request.method == 'POST':
        # Get updated values from the form
        blog.title = request.form['title']
        blog.sub_title = request.form['sub_title']
        blog.content = request.form['content']

        # Update Main Image if a new one is provided
        main_image = request.files['main_image']
        if main_image and allowed_file(main_image.filename):
            filename = secure_filename(main_image.filename)
            main_image.save(os.path.join(app.static_folder, 'uploads', filename))
            blog.main_image_filename = filename

        # Update Image One if a new one is provided
        main_image_one = request.files['main_image_one']
        if main_image_one and allowed_file(main_image_one.filename):
            filename = secure_filename(main_image_one.filename)
            main_image_one.save(os.path.join(app.static_folder, 'uploads', filename))
            blog.main_image_one_filename = filename

        # Update Image Two if a new one is provided
        main_image_two = request.files['main_image_two']
        if main_image_two and allowed_file(main_image_two.filename):
            filename = secure_filename(main_image_two.filename)
            main_image_two.save(os.path.join(app.static_folder, 'uploads', filename))
            blog.main_image_two_filename = filename

        # Commit the changes to the database
        db.session.commit()
        flash('Blog post updated successfully!', 'success')

        return redirect(url_for('dashboard'))

    return render_template('update_blog.html', blog=blog)

@app.route('/deleteblog/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get(blog_id)

    if not blog:
        abort(404)

    if request.method == 'POST':
        # Delete associated images from the file system (optional)
        if blog.main_image_filename:
            os.remove(os.path.join(app.static_folder, 'uploads', blog.main_image_filename))
        if blog.main_image_one_filename:
            os.remove(os.path.join(app.static_folder, 'uploads', blog.main_image_one_filename))
        if blog.main_image_two_filename:
            os.remove(os.path.join(app.static_folder, 'uploads', blog.main_image_two_filename))

        # Delete the blog post from the database
        db.session.delete(blog)
        db.session.commit()
        flash('Blog post deleted successfully!', 'success')

        return redirect(url_for('dashboard'))

    return render_template('delete_blog.html', blog=blog)

# Add this route to your Flask app
# Add this route to your Flask app
@app.route('/add_comment/<int:blog_id>', methods=['POST'])
@login_required
def add_comment(blog_id):
    blog = Blog.query.get(blog_id)

    if not blog:
        abort(404)

    email = request.form.get('email')
    text = request.form.get('comment_text')
    
    # Validate email format
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        flash('Invalid email address!', 'danger')
        return redirect(url_for('view_blog', blog_id=blog.id))

    # Create a new comment
    new_comment = Comment(user=current_user, blog=blog, text=text, email=email)
    db.session.add(new_comment)
    db.session.commit()

    flash('Comment added successfully!', 'success')
    return redirect(url_for('view_blog', blog_id=blog.id))

@app.route('/like/<int:blog_id>')
def like_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog:
        blog.likes += 1
        db.session.commit()
    return redirect(url_for('view_blog', blog_id=blog_id))

@app.route('/share/<int:blog_id>')
def share_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog:
        blog.shares += 1
        db.session.commit()
    return redirect(url_for('view_blog', blog_id=blog_id))



# ...

# Routes for Events
@app.route('/events', methods=['GET'])
def events_list():
    events = Events.query.all()
    return render_template('events_list.html', events=events)
@app.route('/events/<int:event_id>', methods=['GET', 'POST'])
def view_event(event_id):
    event = Events.query.get(event_id)
    category = Events.query.all()  # Corrected the variable name
    
    if not event:
        abort(404)
        
    return render_template('view_event.html', event=event, category=category)


@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Upload Main Image for Event
        main_image = request.files['main_image']
        if main_image and allowed_file(main_image.filename):
            filename = secure_filename(main_image.filename)
            main_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main_image_filename = filename
        else:
            main_image_filename = None

        new_event = Events(title=title, content=content, main_image_filename=main_image_filename)
        db.session.add(new_event)
        db.session.commit()

        flash('Event created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_event.html')

@app.route('/events/<int:event_id>/update', methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Events.query.get(event_id)

    if not event:
        abort(404)

    if request.method == 'POST':
        event.title = request.form['title']
        event.content = request.form['content']

        # Update Main Image if a new one is provided
        main_image = request.files['main_image']
        if main_image and allowed_file(main_image.filename):
            filename = secure_filename(main_image.filename)
            main_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            event.main_image_filename = filename

        db.session.commit()
        flash('Event updated successfully!', 'success')

        return redirect(url_for('dashboard'))

    return render_template('update_event.html', event=event)

@app.route('/events/<int:event_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_event(event_id):
    event = Events.query.get(event_id)

    if not event:
        abort(404)

    if request.method == 'POST':
        # Delete associated image from the file system (optional)
        if event.main_image_filename:
            os.remove(os.path.join(app.static_folder, 'uploads', event.main_image_filename))

        # Delete the event from the database
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully!', 'success')

        return redirect(url_for('dashboard'))

    return render_template('delete_event.html', event=event)

# Routes for Jobs

@app.route('/create_job', methods=['GET', 'POST'])
@login_required
def create_job():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Upload Main Image for Job
        main_image = request.files['main_image']
        if main_image and allowed_file(main_image.filename):
            filename = secure_filename(main_image.filename)
            main_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main_image_filename = filename
        else:
            main_image_filename = None

        new_job = Jobs(title=title, content=content, main_image_filename=main_image_filename)
        db.session.add(new_job)
        db.session.commit()

        flash('Job created successfully!', 'success')
        return redirect(url_for('jobs_list'))

    return render_template('create_job.html')

@app.route('/jobs/<int:job_id>/update', methods=['GET', 'POST'])
@login_required
def update_job(job_id):
    job = Jobs.query.get(job_id)

    if not job:
        abort(404)

    if request.method == 'POST':
        job.title = request.form['title']
        job.content = request.form['content']

        # Update Main Image if a new one is provided
        main_image = request.files['main_image']
        if main_image and allowed_file(main_image.filename):
            filename = secure_filename(main_image.filename)
            main_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            job.main_image_filename = filename

        db.session.commit()
        flash('Job updated successfully!', 'success')

        return redirect(url_for('jobs_list'))

    return render_template('update_job.html', job=job)

@app.route('/jobs/<int:job_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_job(job_id):
    job = Jobs.query.get(job_id)

    if not job:
        abort(404)

    if request.method == 'POST':
        # Delete associated image from the file system (optional)
        if job.main_image_filename:
            os.remove(os.path.join(app.static_folder, 'uploads', job.main_image_filename))

        # Delete the job from the database
        db.session.delete(job)
        db.session.commit()
        flash('Job deleted successfully!', 'success')

        return redirect(url_for('jobs_list'))

    return render_template('delete_job.html', job=job)

@app.route('/upload_publication', methods = ['GET', 'POST'])
@login_required
def publication():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        main_image = request.files['main_image']
        if main_image and allowed_file(main_image.filename):
            filename = secure_filename(main_image.filename)
            main_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main_image_filename = filename
        else:
            main_image_filename = None
        new_pub = Publication(title= title, content= content, main_image_filename = main_image_filename)
        db.session.add(new_pub)
        db.session.commit()
        
        flash ('New Publication created!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_pub.html')

@app.route('/publications', methods=['GET'])
def pub_list():
    publications = Publication.query.all()
    return render_template('pub_list.html', publications = publications )

@app.route('/publications/<int:publication_id>', methods = ['GET', 'POST'])
def view_publication(publication_id):
    publication = Publication.query.get(publication_id)
    publication_list = Publication.query.all()
    
    if not publication:
        abort(404)
        
    return render_template('view_pub.html', publication=publication,publication_list= publication_list )

@app.route('/publications/<int:publication_id>/update', methods=['GET', 'POST'])
@login_required
def update_publication(publication_id):
    publication = Publication.query.get(publication_id)

    if not publication:
        abort(404)

    if request.method == 'POST':
        publication.title = request.form['title']
        publication.content = request.form['content']

        # Update Main Image if a new one is provided
        main_image = request.files['main_image']
        if main_image and allowed_file(main_image.filename):
            filename = secure_filename(main_image.filename)
            main_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            publication.main_image_filename = filename

        db.session.commit()
        flash('Publication updated successfully!', 'success')

        return redirect(url_for('dashboard'))

    return render_template('update_publication.html', publication=publication)

@app.route('/publication/<int:publication_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_publication(publication_id):
    publication = Publication.query.get(publication_id)

    if not publication:
        abort(404)

    if request.method == 'POST':
        # Delete associated image from the file system (optional)
        if publication.main_image_filename:
            os.remove(os.path.join(app.static_folder, 'uploads', publication.main_image_filename))

        # Delete the event from the database
        db.session.delete(publication)
        db.session.commit()
        flash('Publication deleted successfully!', 'success')

        return redirect(url_for('dashboard'))

    return render_template('delete_pub.html', publication=publication)

@app.route('/upload_gallery', methods = ['GET', 'POST'])
@login_required
def gallery():
    if request.method == 'POST':
        description = request.form['description']
        main_image = request.files['main_image']
        if main_image and allowed_file(main_image.filename):
            filename = secure_filename(main_image.filename)
            main_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main_image_filename = filename
        else:
            main_image_filename = None
        new_gallery = Gallery(description= description, main_image_filename = main_image_filename)
        db.session.add(new_gallery)
        db.session.commit()
        
        flash ('New Picture uploaded!', 'success')
        return redirect(url_for('gallery_list'))
    
    return render_template('create_gallery.html')

@app.route('/gallery/<int:gallery_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_gallery(gallery_id):
    gallery = Gallery.query.get(gallery_id)

    if not gallery:
        abort(404)

    if request.method == 'POST':
        # Delete associated image from the file system (optional)
        if gallery.main_image_filename:
            os.remove(os.path.join(app.static_folder, 'uploads', gallery.main_image_filename))

        # Delete the event from the database
        db.session.delete(gallery)
        db.session.commit()
        flash('Gallery deleted successfully!', 'success')

        return redirect(url_for('gallery_list'))

    return render_template('delete_gallery.html', gallery=gallery)

@app.route('/')
def index():
    category = Publication.query.all()
    blogs = Blog.query.all()
    
    
    return render_template('index.html', category=category, blogs = blogs)


@app.route('/about')
def about():
    return render_template('about.html') 
@app.route('/book')
def book():
    return render_template('book.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/author')
def author():
    return render_template('author.html')

@app.route('/topseller')
def topseller():
    return render_template('top-seller.html')

@app.route('/nav')
def nav():
    return render_template('nav.html')
@app.route('/header')
def header():
    return render_template('header.html')
@app.route('/footer')
def footer():
    return render_template('footer.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/mission')
def mission():
    return render_template('mission-vision.html')

@app.route('/team')
def team():
    return render_template('team-members.html')

@app.route('/releases')
def releases():
    blogs = Blog.query.all()
    return render_template('press-releases.html', blogs = blogs)

@app.route('/clients')
def clients():
    return render_template('clients.html')

@app.route('/career')
def career():
    return render_template('career.html')

@app.route('/business/development')
def business_development():
    return render_template('solutions01.html')

@app.route('/partner/investment')
def partner_investment():
    return render_template('solutions02.html')

@app.route('/consultation')
def consultation():
    return render_template('solutions05.html')

# @app.route('/career')
# def career():
#     return render_template('solutions06.html')

@app.route('/training')
def traning():
    return render_template('solutions07.html')

@app.route('/management')
def management():
    return render_template('solutions08.html')

@app.route('/showcase')
def showcase():
    return render_template('showcases.html')


@app.route('/startup')
def startup():
    return render_template('solutions09.html')


@app.route('/news/single')
def news_single():
    blogs = Blog.query.all()

    return render_template('press-releases.html', blogs = blogs)


@app.route('/news/left')
def news_left():
    events = Events.query.all()
    return render_template('news-sidebar-left.html', events=events)


@app.route('/news/right')
def news_right():
    publications = Publication.query.all()
    return render_template('news-sidebar-right.html', publications = publications)


@app.route('/news/noside')
def news_sidebar():
    return render_template('news-sidebar-nosidebar.html')


@app.route('/gallery')
def news_single_left():
    return render_template('news-single-sidebar-left.html')


@app.route('/godson')
def about_godson():
    return render_template('news-single-sidebar-right.html')


@app.route('/joy')
def about_joy():
    return render_template('joy.html')


@app.route('/chibuzo')
def about_chibuzo():
    return render_template('chibuzo.html')

@app.route('/kishan')
def about_kishan():
    return render_template('kishan.html')


@app.route('/steve')
def about_steve():
    return render_template('steve.html')



@app.route('/adminbloglist')
@login_required
def adminbloglist():
    blog = Blog.query.all()
    return render_template('adminblog_list.html', blog = blog)


@app.route('/admineventlist')
@login_required
def admineventlist():
    event = Events.query.all()
    return render_template('adminevent_list.html', event = event)



@app.route('/adminpublist')
@login_required
def adminpublist():
    publication = Publication.query.all()
    return render_template('adminpub_list.html', publication = publication)

# @app.route("/backup_db")
# @login_required
# def backup_database():
#     backup_folder = "backup/"
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     backup_filename = f"backup_{timestamp}.db"

#     # Create the backup folder if it doesn't exist
#     if not os.path.exists(backup_folder):
#         os.makedirs(backup_folder)

#     # Copy the database file to the backup folder
#     shutil.copy("your_database.db", os.path.join(backup_folder, backup_filename))

#     return f"Database backup created: {backup_filename}"



@app.route("/db/offload")
@login_required

def database():
    db.drop_all()
    db.create_all()
    migrate.init_app(app, db)
    return "Database reset and migration completed!"
    

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5500, debug=True)