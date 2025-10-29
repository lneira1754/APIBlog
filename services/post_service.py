from repositories.post_repository import PostRepository
from repositories.category_repository import CategoryRepository

class PostService:
    def __init__(self):
        self.post_repo = PostRepository()
        self.category_repo = CategoryRepository()
    
    def get_public_posts(self):
        return self.post_repo.get_all_published()
    
    def get_all_posts(self):
        return self.post_repo.get_all()
    
    def get_post_by_id(self, post_id):
        return self.post_repo.get_by_id(post_id)
    
    def get_user_posts(self, user_id):
        return self.post_repo.get_user_posts(user_id)
    
    def create_post(self, post_data, user_id):
        #validar categorías si existen
        if 'categories' in post_data:
            valid_categories = []
            for cat_id in post_data['categories']:
                category = self.category_repo.get_by_id(cat_id)
                if category:
                    valid_categories.append(cat_id)
            post_data['categories'] = valid_categories
        
        return self.post_repo.create(post_data, user_id)
    
    def update_post(self, post, post_data):
        if 'categories' in post_data:
            valid_categories = []
            for cat_id in post_data['categories']:
                category = self.category_repo.get_by_id(cat_id)
                if category:
                    valid_categories.append(cat_id)
            post_data['categories'] = valid_categories
        
        return self.post_repo.update(post, post_data)
    
    def delete_post(self, post):
        self.post_repo.delete(post)