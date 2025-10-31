from flask import Blueprint, request, jsonify
from flask.views import MethodView
from schemas.user_schema import UserSchema, UserLoginSchema
from services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity
from repositories.user_repository import UserRepository

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()
login_schema = UserLoginSchema()
auth_service = AuthService()
user_repo = UserRepository()

class RegisterAPI(MethodView):
    def post(self):
        try:
            #validar datos de entrada
            errors = user_schema.validate(request.json)
            if errors:
                return jsonify({'errores': errors}), 400
            
            user_data = user_schema.load(request.json)
            user, error = auth_service.register_user(user_data)
            
            if error:
                return jsonify({'error': error}), 400
            
            return jsonify({
                'mensaje': 'Usuario creado exitosamente',
                'user_id': user.id
            }), 201
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500

class LoginAPI(MethodView):
    def post(self):
        try:
            #validar datos de entrada
            errors = login_schema.validate(request.json)
            if errors:
                return jsonify({'errores': errors}), 400
            
            data = login_schema.load(request.json)
            result, error = auth_service.login_user(data['email'], data['password'])
            
            if error:
                return jsonify({'error': error}), 401
            
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500

class ProfileAPI(MethodView):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            #el user_id ahora es string, convertir a int para la consulta
            user = user_repo.get_by_id(int(user_id))
            

            
            if not user:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            
            return jsonify(user.to_dict()), 200
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500

#registro de rutas de las paginas
auth_bp.add_url_rule('/register', view_func=RegisterAPI.as_view('register'))
auth_bp.add_url_rule('/login', view_func=LoginAPI.as_view('login'))
auth_bp.add_url_rule('/profile', view_func=ProfileAPI.as_view('profile'))