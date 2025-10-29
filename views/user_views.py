from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from schemas.user_schema import UserUpdateSchema
from services.user_service import UserService
from decorators.roles import admin_required

user_bp = Blueprint('users', __name__)
user_update_schema = UserUpdateSchema()
user_service = UserService()
#
class UserListAPI(MethodView):
    @jwt_required()
    @admin_required
    def get(self):
        try:
            users = user_service.get_all_users()
            return jsonify([user.to_dict() for user in users]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

class UserDetailAPI(MethodView):
    @jwt_required()
    def get(self, user_id):
        try:
            claims = get_jwt()
            current_user_id = claims.get('user_id')
            current_user_role = claims.get('role')
            
            #solo el usuario mismo o admin puede ver los detalles
            if current_user_role != 'admin' and current_user_id != user_id:
                return jsonify({'error': 'No tienes permisos para ver este usuario'}), 403
            
            user = user_service.get_user_by_id(user_id)
            if not user:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            
            return jsonify(user.to_dict()), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

class UserRoleAPI(MethodView):
    @jwt_required()
    @admin_required
    def patch(self, user_id):
        try:
            user = user_service.get_user_by_id(user_id)
            if not user:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            
            new_role = request.json.get('role')
            if not new_role or new_role not in ['user', 'moderator', 'admin']:
                return jsonify({'error': 'Rol inválido'}), 400
            
            updated_user = user_service.update_user_role(user_id, new_role)
            
            return jsonify({
                'message': f'Rol actualizado a {new_role}',
                'user': updated_user.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

class UserStatusAPI(MethodView):
    @jwt_required()
    @admin_required
    def patch(self, user_id):
        try:
            user = user_service.get_user_by_id(user_id)
            if not user:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            
            is_active = request.json.get('is_active')
            if is_active is None:
                return jsonify({'error': 'Campo is_active requerido'}), 400
            
            updated_user = user_service.update_user_status(user_id, is_active)
            
            status = 'activado' if is_active else 'desactivado'
            return jsonify({
                'message': f'Usuario {status} exitosamente',
                'user': updated_user.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

#registrar rutas
user_bp.add_url_rule('/users', view_func=UserListAPI.as_view('users'))
user_bp.add_url_rule('/users/<int:user_id>', view_func=UserDetailAPI.as_view('user_detail'))
user_bp.add_url_rule('/users/<int:user_id>/role', view_func=UserRoleAPI.as_view('user_role'))
user_bp.add_url_rule('/users/<int:user_id>/status', view_func=UserStatusAPI.as_view('user_status'))