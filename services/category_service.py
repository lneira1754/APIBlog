from repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self):
        self.category_repo = CategoryRepository()
    
    def get_all_categories(self):
        return self.category_repo.get_all()
    
    def get_category_by_id(self, category_id):
        return self.category_repo.get_by_id(category_id)
    
    def get_category_by_name(self, name):
        return self.category_repo.get_by_name(name)
    
    def create_category(self, category_data):
        return self.category_repo.create(category_data)
    
    def update_category(self, category, category_data):
        return self.category_repo.update(category, category_data)
    
    def delete_category(self, category):
        self.category_repo.delete(category)