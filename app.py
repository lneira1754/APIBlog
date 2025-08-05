from flask import Flask, flash, render_template, request, redirect, url_for
from extensions import db, login_manager, migrate
from models import User, Post, Comment, Category 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Post, Comment, Category

app = Flask(__name__)

app.secret_key = "cualquiercosa"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/miniblog_flask"

db.init_app(app)
login_manager.init_app(app)
migrate.init_app(app, db)
login_manager.login_view = "login"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_categories():
    categories = Category.query.all()
    return dict(categories=categories)

@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Usuario o contraseña incorrectos', 'error')
    return render_template("auth/login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Nombre de usuario ya existe', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email ya registrado', 'error')
            return redirect(url_for('register'))
        
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template("auth/register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#ruta blog
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_ids = request.form.getlist('categories')
        
        post = Post(
            title=title,
            content=content,
            author=current_user
        )
        
        for cat_id in category_ids:
            category = Category.query.get(cat_id)
            if category:
                post.categories.append(category)
        
        db.session.add(post)
        db.session.commit()
        flash('Post creado exitosamente!', 'success')
        return redirect(url_for('index'))
    
    return render_template('blog/new_post.html')

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blog/post_detail.html', post=post)

@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    text = request.form['text']
    
    comment = Comment(
        text=text,
        author=current_user,
        post=post
    )
    
    db.session.add(comment)
    db.session.commit()
    flash('Comentario agregado!', 'success')
    return redirect(url_for('post_detail', post_id=post.id))

@app.route('/category/<int:category_id>')
def category_posts(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template('blog/category_posts.html', category=category) 

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    flash('El post fue eliminado correctamente.')
    return redirect(url_for('index'))  # o donde quieras redirigir


@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Solo el autor puede editar
    if post.author != current_user:
        flash('No tenés permiso para editar este post.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        category_ids = request.form.getlist('categories')
        post.categories = [Category.query.get(cat_id) for cat_id in category_ids if Category.query.get(cat_id)]
        db.session.commit()
        flash('Post actualizado con éxito!', 'success')
        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('blog/edit_post.html', post=post)


with app.app_context():
    if Category.query.count() == 0:
        categorias = ['Tecnología', 'Ciencia', 'Arte', 'Opinión', 'Noticias']
        for nombre in categorias:
            db.session.add(Category(name=nombre))
        db.session.commit()
        print("Categorías iniciales creadas.")


if __name__ == '__main__':
    app.run(debug=True)