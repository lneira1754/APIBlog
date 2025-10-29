from flask import Blueprint, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from services.stats_service import StatsService
from decorators.roles import roles_required

stats_bp = Blueprint('stats', __name__)
stats_service = StatsService()

class StatsAPI(MethodView):
    @jwt_required()
    @roles_required('admin', 'moderator')
    def get(self):
        try:
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role == 'admin':
                stats = stats_service.get_detailed_stats()
            else:
                stats = stats_service.get_basic_stats()
            
            return jsonify(stats), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

#registrar rutas
stats_bp.add_url_rule('/stats', view_func=StatsAPI.as_view('stats'))