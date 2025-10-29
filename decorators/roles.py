from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity  # Agregar get_jwt_identity

def roles_required(*required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role not in required_roles:
                return jsonify({'error': 'Permisos insuficientes'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return roles_required('admin')(f)

def moderator_required(f):
    return roles_required('admin', 'moderator')(f)

def check_ownership(resource_user_id):
    """Verifica si el usuario es dueño del recurso o es admin"""
    verify_jwt_in_request()
    claims = get_jwt()
    current_user_id = int(get_jwt_identity())  #convertir a entero
    user_role = claims.get('role')
    
    return user_role == 'admin' or current_user_id == resource_user_id