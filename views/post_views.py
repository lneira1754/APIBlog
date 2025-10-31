from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from schemas.post_schema import PostSchema, PostUpdateSchema
from services.post_service import PostService
from decorators.roles import roles_required, check_ownership

post_bp = Blueprint('posts', __name__)
post_schema = PostSchema()
post_update_schema = PostUpdateSchema()
post_service = PostService()

class PostListAPI(MethodView):
    def get(self):
        try:
            posts = post_service.get_public_posts()
            return jsonify([post.to_dict() for post in posts]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    def post(self):
        try:
            # Validar datos
            errors = post_schema.validate(request.json)
            if errors:
                return jsonify({'errors': errors}), 400
            
            user_id = get_jwt_identity()
            post_data = post_schema.load(request.json)
            post = post_service.create_post(post_data, user_id)
            
            return jsonify(post.to_dict()), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

class PostDetailAPI(MethodView):
    def get(self, post_id):
        try:
            post = post_service.get_post_by_id(post_id)
            if not post or (not post.is_published and not self._can_edit_post(post)):
                return jsonify({'error': 'Post no encontrado'}), 404
            
            return jsonify(post.to_dict()), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    def put(self, post_id):
        try:
            post = post_service.get_post_by_id(post_id)
            if not post:
                return jsonify({'error': 'Post no encontrado'}), 404
            
            #vrificar permisos
            if not check_ownership(post.user_id):
                return jsonify({'error': 'No tienes permisos para editar este post'}), 403
            
            #validar datos
            errors = post_update_schema.validate(request.json)
            if errors:
                return jsonify({'errors': errors}), 400
            
            post_data = post_update_schema.load(request.json)
            updated_post = post_service.update_post(post, post_data)
            
            return jsonify(updated_post.to_dict()), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    def delete(self, post_id):
        try:
            post = post_service.get_post_by_id(post_id)
            if not post:
                return jsonify({'error': 'Post no encontrado'}), 404
            
            #vrificar permisos - autor o admin
            claims = get_jwt()
            if claims.get('role') != 'admin' and post.user_id != get_jwt_identity():
                return jsonify({'error': 'No tienes permisos para eliminar este post'}), 403
            
            post_service.delete_post(post)
            
            return jsonify({'mensaje': 'Post eliminado exitosamente'}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def _can_edit_post(self, post):
        """Verifica si el usuario actual puede ver posts no publicados"""
        try:
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request()
            claims = get_jwt()
            return claims.get('role') in ['admin', 'moderator'] or post.user_id == get_jwt_identity()
        except:
            return False

class UserPostsAPI(MethodView):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            posts = post_service.get_user_posts(user_id)
            return jsonify([post.to_dict() for post in posts]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

#registrar rutas
post_bp.add_url_rule('/posts', view_func=PostListAPI.as_view('posts'))
post_bp.add_url_rule('/posts/<int:post_id>', view_func=PostDetailAPI.as_view('post_detail'))
post_bp.add_url_rule('/my-posts', view_func=UserPostsAPI.as_view('user_posts'))