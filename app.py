from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

#configuracion de la base de datos y secret key
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/miniblog_flask')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'tu-clave-secreta-aqui')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secreto-muy-seguro')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400 #horas en segundos

#configuraciones del JWT
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

#configuracion de errores del JWT
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token ha expirado (24 Horas)'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Token invalido', 'detalle': str(error)}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Token requerido'}), 401
#error cuando el token necesita ser renovado
@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token necesita ser nuevo'}), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token ha sido revocado'}), 401

#importamos modelos después de db y migrate
from models.user import User
from models.post import Post
from models.comment import Comment
from models.category import Category
from models.post_category import post_category

#importamos y registramos blueprints
from views.auth_views import auth_bp
from views.post_views import post_bp
from views.comment_views import comment_bp
from views.category_views import category_bp
from views.user_views import user_bp
from views.stats_views import stats_bp

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(post_bp, url_prefix='/api')
app.register_blueprint(comment_bp, url_prefix='/api')
app.register_blueprint(category_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(stats_bp, url_prefix='/api')

#ruta de prueba
@app.route('/')
def index():
    return jsonify({'mensaje': 'API del MiniBlog funcionando'})

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'mensaje': 'API funciona correctamente'})

if __name__ == '__main__':
    app.run(debug=True)
