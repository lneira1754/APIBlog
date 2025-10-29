from app import db
from models.comment import Comment
from sqlalchemy import desc

class CommentRepository:
    @staticmethod
    def get_by_post_id(post_id):
        return Comment.query.filter_by(post_id=post_id, is_visible=True).order_by(desc(Comment.created_at)).all()
    
    @staticmethod
    def get_by_id(comment_id):
        return Comment.query.get(comment_id)
    
    @staticmethod
    def create(comment_data, user_id):
        comment = Comment(
            text=comment_data['text'],
            user_id=user_id,
            post_id=comment_data['post_id']
        )
        db.session.add(comment)
        db.session.commit()
        return comment
    
    @staticmethod
    def delete(comment):
        db.session.delete(comment)
        db.session.commit()
    
    @staticmethod
    def hide(comment):
        comment.is_visible = False
        db.session.commit()
        return comment