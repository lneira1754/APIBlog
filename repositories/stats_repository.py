from app import db
from models.user import User
from models.post import Post
from models.comment import Comment
from sqlalchemy import func
from datetime import datetime, timedelta

class StatsRepository:
    @staticmethod
    def get_basic_stats():
        # Contar solo posts NO eliminados
        total_posts = Post.query.filter_by(deleted=False).count()
        
        # Contar todos los comentarios (incluyendo los de posts eliminados)
        # Si quieres solo comentarios de posts activos, cambia a:
        total_comments = Comment.query.join(Post).filter(Post.deleted == False).count()
        #total_comments = Comment.query.count()
        
        # Contar todos los usuarios activos
        total_users = User.query.filter_by(is_active=True).count()
        
        return {
            'total_posts': total_posts,
            'total_comments': total_comments,
            'total_users': total_users
        }
    
    @staticmethod
    def get_detailed_stats():
        basic_stats = StatsRepository.get_basic_stats()
        
        # Posts de la última semana (solo NO eliminados)
        week_ago = datetime.utcnow() - timedelta(days=7)
        posts_last_week = Post.query.filter(
            Post.created_at >= week_ago,
            Post.deleted == False
        ).count()
        
        # Usuarios por rol (solo activos)
        users_by_role = {
            'admin': User.query.filter_by(role='admin', is_active=True).count(),
            'moderator': User.query.filter_by(role='moderator', is_active=True).count(),
            'user': User.query.filter_by(role='user', is_active=True).count()
        }
        
        # Posts por categoría (solo NO eliminados)
        from models.category import Category
        categories_with_counts = db.session.query(
            Category.name, 
            func.count(Post.id)
        ).join(
            Category.posts
        ).filter(
            Post.deleted == False  # Excluir posts eliminados
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