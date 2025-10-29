from repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    def get_all_users(self):
        return self.user_repo.get_all()
    
    def get_user_by_id(self, user_id):
        return self.user_repo.get_by_id(user_id)
    
    def update_user_role(self, user_id, new_role):
        return self.user_repo.update_role(user_id, new_role)
    
    def update_user_status(self, user_id, is_active):
        user = self.user_repo.get_by_id(user_id)
        if user:
            user.is_active = is_active
            from app import db
            db.session.commit()
        return user