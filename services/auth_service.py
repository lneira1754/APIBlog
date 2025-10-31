from repositories.user_repository import UserRepository
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    def register_user(self, user_data):
        #vrificar si el usuario ya existe en la bd
        if self.user_repo.get_by_email(user_data['email']):
            return None, 'El email ya esta registrado'
        
        if self.user_repo.get_by_username(user_data['username']):
            return None, 'El nombre de usuario ya existe'
        
        user = self.user_repo.create(user_data)
        return user, None
    
    def login_user(self, email, password):
        user = self.user_repo.get_by_email(email)
        if not user or not check_password_hash(user.password_hash, password):
            return None, 'Credenciales invalidas'
        
        if not user.is_active:
            return None, 'Usuario desactivado'
        
        #crear token en jwt
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'email': user.email,
                'role': user.role,
                'username': user.username
            }
        )
        
        return {
            'access_token': access_token,
            'user': user.to_dict()
        }, None