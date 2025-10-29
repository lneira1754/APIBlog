from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from schemas.category_schema import CategorySchema
from services.category_service import CategoryService
from decorators.roles import roles_required

category_bp = Blueprint('categories', __name__)
category_schema = CategorySchema()
category_service = CategoryService()

class CategoryListAPI(MethodView):
    def get(self):
        try:
            categories = category_service.get_all_categories()
            return jsonify([category.to_dict() for category in categories]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    @roles_required('admin', 'moderator')
    def post(self):
        try:
            #validar datos
            errors = category_schema.validate(request.json)
            if errors:
                return jsonify({'errors': errors}), 400
            
            category_data = category_schema.load(request.json)
            
            #verificar si la categoría ya existe antes de crearla
            existing_category = category_service.get_category_by_name(category_data['name'])
            if existing_category:
                return jsonify({'error': 'La categoria ya existe'}), 400
            
            category = category_service.create_category(category_data)
            
            return jsonify(category.to_dict()), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

class CategoryDetailAPI(MethodView):
    def get(self, category_id):
        try:
            category = category_service.get_category_by_id(category_id)
            if not category:
                return jsonify({'error': 'Categoria no encontrada'}), 404
            
            return jsonify(category.to_dict()), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    @roles_required('admin', 'moderator')
    def put(self, category_id):
        try:
            category = category_service.get_category_by_id(category_id)
            if not category:
                return jsonify({'error': 'Categoria no encontrada'}), 404
            
            #validar datos
            errors = category_schema.validate(request.json)
            if errors:
                return jsonify({'errors': errors}), 400
            
            category_data = category_schema.load(request.json)
            
            #verificar si la categoriia ya existe
            existing_category = category_service.get_category_by_name(category_data['name'])
            if existing_category and existing_category.id != category_id:
                return jsonify({'error': 'Ya existe una categoria con ese nombre'}), 400
            
            updated_category = category_service.update_category(category, category_data)
            
            return jsonify(updated_category.to_dict()), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    @roles_required('admin')
    def delete(self, category_id):
        try:
            category = category_service.get_category_by_id(category_id)
            if not category:
                return jsonify({'error': 'Categoria no encontrada'}), 404
            #verificamos si la categoria tiene posteos
            if category.posts:
                return jsonify({'error': 'No se puede eliminar una categoria con posts creados'}), 400
            
            category_service.delete_category(category)
            
            return jsonify({'message': 'Categoria eliminada exitosamente'}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Registrar rutas
category_bp.add_url_rule('/categories', view_func=CategoryListAPI.as_view('categories'))
category_bp.add_url_rule('/categories/<int:category_id>', view_func=CategoryDetailAPI.as_view('category_detail'))