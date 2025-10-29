from app import db
from models.category import Category

class CategoryRepository:
    @staticmethod
    def get_all():
        return Category.query.all()
    
    @staticmethod
    def get_by_id(category_id):
        return Category.query.get(category_id)
    
    @staticmethod
    def get_by_name(name):
        return Category.query.filter_by(name=name).first()
    
    @staticmethod
    def create(category_data):
        category = Category(name=category_data['name'])
        db.session.add(category)
        db.session.commit()
        return category
    
    @staticmethod
    def update(category, category_data):
        category.name = category_data['name']
        db.session.commit()
        return category
    
    @staticmethod
    def delete(category):
        db.session.delete(category)
        db.session.commit()