from app import db
from models.post import Post
from models.category import Category
from models.comment import Comment
from sqlalchemy import desc

class PostRepository:
    @staticmethod
    def get_all_published():
        # Solo posts no eliminados
        return Post.query.filter_by(is_published=True, deleted=False).order_by(desc(Post.created_at)).all()
    
    @staticmethod
    def get_all():
        # Solo posts no eliminados
        return Post.query.filter_by(deleted=False).order_by(desc(Post.created_at)).all()
    
    @staticmethod
    def get_by_id(post_id):
        # Traer incluso posts eliminados (para que admin pueda ver)
        return Post.query.get(post_id)
    
    @staticmethod
    def get_user_posts(user_id):
        # Solo posts no eliminados del usuario
        return Post.query.filter_by(user_id=user_id, deleted=False).order_by(desc(Post.created_at)).all()
    
    @staticmethod
    def create(post_data, user_id):
        post = Post(
            title=post_data['title'],
            content=post_data['content'],
            user_id=user_id,
            is_published=post_data.get('is_published', True),
            deleted=False  # Asegurar que no esté eliminado
        )
        
        if 'categories' in post_data:
            categories = Category.query.filter(Category.id.in_(post_data['categories'])).all()
            post.categories.extend(categories)
        
        db.session.add(post)
        db.session.commit()
        return post
    
    @staticmethod
    def update(post, post_data):
        if 'title' in post_data:
            post.title = post_data['title']
        if 'content' in post_data:
            post.content = post_data['content']
        if 'is_published' in post_data:
            post.is_published = post_data['is_published']
        
        if 'categories' in post_data:
            post.categories = []
            categories = Category.query.filter(Category.id.in_(post_data['categories'])).all()
            post.categories.extend(categories)
        
        db.session.commit()
        return post
    
    @staticmethod
    def delete(post):
        # SOFT DELETE - solo marcar como eliminado
        post.deleted = True
        post.is_published = False  # También ocultar de publicaciones
        db.session.commit()
        return post