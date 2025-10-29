import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models.user import User
from werkzeug.security import generate_password_hash
#Este codigo lo hice con chatgpt para probar la creacion de usuarios mas rapida xd
def create_test_users():
    with app.app_context():
        users = [
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password': 'admin123',
                'role': 'admin'
            },
            {
                'username': 'moderator1',
                'email': 'moderator@example.com', 
                'password': 'mod123',
                'role': 'moderator'
            },
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'password': 'user123',
                'role': 'user'
            }
        ]
        
        
        for user_data in users:
            # Verificar si el usuario ya existe
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user:
                print(f"⚠️  Usuario {user_data['username']} ya existe")
                continue
            
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password']),
                role=user_data['role']
            )
            db.session.add(user)
            print(f"✅ Usuario {user_data['username']} creado")
        
        db.session.commit()
        print("\n🎉 Todos los usuarios creados exitosamente!")

if __name__ == '__main__':
    create_test_users()