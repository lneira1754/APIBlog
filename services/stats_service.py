from repositories.stats_repository import StatsRepository

class StatsService:
    def __init__(self):
        self.stats_repo = StatsRepository()
    
    def get_basic_stats(self):
        return self.stats_repo.get_basic_stats()
    
    def get_detailed_stats(self):
        return self.stats_repo.get_detailed_stats()