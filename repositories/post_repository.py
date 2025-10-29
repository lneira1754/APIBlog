from app import db
from models.post import Post
from models.category import Category
from sqlalchemy import desc

class PostRepository:
    @staticmethod
    def get_all_published():
        return Post.query.filter_by(is_published=True).order_by(desc(Post.created_at)).all()
    
    @staticmethod
    def get_all():
        return Post.query.order_by(desc(Post.created_at)).all()
    
    @staticmethod
    def get_by_id(post_id):
        return Post.query.get(post_id)
    
    @staticmethod
    def get_user_posts(user_id):
        return Post.query.filter_by(user_id=user_id).order_by(desc(Post.created_at)).all()
    
    @staticmethod
    def create(post_data, user_id):
        post = Post(
            title=post_data['title'],
            content=post_data['content'],
            user_id=user_id,
            is_published=post_data.get('is_published', True)
        )
        
        # Agregar categorías si se proporcionan
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
        
        #actualizar categorías si se proporcionan
        if 'categories' in post_data:
            post.categories = []
            categories = Category.query.filter(Category.id.in_(post_data['categories'])).all()
            post.categories.extend(categories)
        
        db.session.commit()
        return post
    
    @staticmethod
    def delete(post):
        db.session.delete(post)
        db.session.commit()