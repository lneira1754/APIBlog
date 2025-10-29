from repositories.comment_repository import CommentRepository

class CommentService:
    def __init__(self):
        self.comment_repo = CommentRepository()
    
    def get_post_comments(self, post_id):
        return self.comment_repo.get_by_post_id(post_id)
    
    def get_comment_by_id(self, comment_id):
        return self.comment_repo.get_by_id(comment_id)
    
    def create_comment(self, comment_data, user_id):
        comment_data['user_id'] = user_id
        return self.comment_repo.create(comment_data, user_id)
    
    def delete_comment(self, comment):
        self.comment_repo.delete(comment)
    
    def hide_comment(self, comment):
        self.comment_repo.hide(comment)