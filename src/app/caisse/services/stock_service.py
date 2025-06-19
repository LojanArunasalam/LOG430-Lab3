from caisse.repositories.stock_repository import StockRepository

class StockService: 
    def __init__(self, session):
        self.session = session
        self.stock_repository = StockRepository(session)

    
