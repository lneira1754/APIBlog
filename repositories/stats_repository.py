from app import db
from models.user import User
from models.post import Post
from models.comment import Comment
from sqlalchemy import func
from datetime import datetime, timedelta

class StatsRepository:
    @staticmethod
    def get_basic_stats():
        total_posts = Post.query.count()
        total_comments = Comment.query.count()
        total_users = User.query.count()
        
        return {
            'total_posts': total_posts,
            'total_comments': total_comments,
            'total_users': total_users
        }
    
    @staticmethod
    def get_detailed_stats():
        basic_stats = StatsRepository.get_basic_stats()
        
        #posts de la última semana
        week_ago = datetime.utcnow() - timedelta(days=7)
        posts_last_week = Post.query.filter(Post.created_at >= week_ago).count()
        
        #usuarios por rol (ahora usando string directamente)
        users_by_role = {
            'admin': User.query.filter_by(role='admin').count(),
            'moderator': User.query.filter_by(role='moderator').count(),
            'user': User.query.filter_by(role='user').count()
        }
        
        #posts por categoría
        from models.category import Category
        categories_with_counts = db.session.query(
            Category.name, 
            func.count(Post.id)
        ).join(
            Category.posts
        ).group_by(
            Category.id
        ).all()
        
        posts_by_category = {cat[0]: cat[1] for cat in categories_with_counts}
        
        basic_stats.update({
            'posts_last_week': posts_last_week,
            'users_by_role': users_by_role,
            'posts_by_category': posts_by_category
        })
        
        return basic_stats