from app import db
from models.user import User
from werkzeug.security import generate_password_hash

class UserRepository:
    @staticmethod
    def get_all():
        return User.query.all()
    
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def create(user_data):
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password_hash=generate_password_hash(user_data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_role(user_id, new_role):
        user = User.query.get(user_id)
        if user:
            user.role = new_role
            db.session.commit()
        return user