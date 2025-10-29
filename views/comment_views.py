from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from schemas.comment_schema import CommentSchema
from services.comment_service import CommentService
from services.post_service import PostService
from decorators.roles import roles_required, check_ownership

comment_bp = Blueprint('comments', __name__)
comment_schema = CommentSchema()
comment_service = CommentService()
post_service = PostService()

class CommentListAPI(MethodView):
    def get(self, post_id):
        try:
            #verificar que el post existe
            post = post_service.get_post_by_id(post_id)
            if not post:
                return jsonify({'error': 'Post no encontrado'}), 404
            
            comments = comment_service.get_post_comments(post_id)
            return jsonify([comment.to_dict() for comment in comments]), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    def post(self, post_id):
        try:
            #verificar que el post existe
            post = post_service.get_post_by_id(post_id)
            if not post:
                return jsonify({'error': 'Post no encontrado'}), 404
            
            #validar datos
            errors = comment_schema.validate(request.json)
            if errors:
                return jsonify({'errors': errors}), 400
            
            user_id = get_jwt_identity()
            comment_data = comment_schema.load(request.json)
            comment_data['post_id'] = post_id
            
            comment = comment_service.create_comment(comment_data, user_id)
            
            return jsonify(comment.to_dict()), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

class CommentDetailAPI(MethodView):
    @jwt_required()
    def delete(self, comment_id):
        try:
            comment = comment_service.get_comment_by_id(comment_id)
            if not comment:
                return jsonify({'error': 'Comentario no encontrado'}), 404
            
            claims = get_jwt()
            user_id = get_jwt_identity()
            user_role = claims.get('role')
            
            #verificar permisos: autor, moderator o admin
            can_delete = (
                user_role in ['admin', 'moderator'] or 
                check_ownership(comment.user_id)
            )
            
            if not can_delete:
                return jsonify({'error': 'No tienes permisos para eliminar este comentario'}), 403
            
            #los moderadores solo pueden ocultar, no eliminar(solo admin)
            if user_role == 'moderator' and not check_ownership(comment.user_id):
                comment_service.hide_comment(comment)
                return jsonify({'message': 'Comentario ocultado exitosamente'}), 200
            else:
                #el autor o admin pueden eliminar completamente
                comment_service.delete_comment(comment)
                return jsonify({'message': 'Comentario eliminado exitosamente'}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Registrar rutas
comment_bp.add_url_rule('/posts/<int:post_id>/comments', view_func=CommentListAPI.as_view('post_comments'))
comment_bp.add_url_rule('/comments/<int:comment_id>', view_func=CommentDetailAPI.as_view('comment_detail'))