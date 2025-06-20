import logging
from ..models import Product, LineSale, Sale, Store, Product_Depot
from ..repositories.product_repository import ProductRepository
from ..repositories.sale_repository import SaleRepository
from ..repositories.stock_repository import StockRepository

class DomainService: 
    def __init__(self, session):
        self.session = session
        self.product_repository = ProductRepository(session)
        self.sale_repository = SaleRepository(session)
        self.stock_repository = StockRepository(session)


    def restock_from_depot(self, product_id, quantity, store_id):
        stock = self.stock_repository.get_stock_by_product_and_store(self.session, product_id, store_id)
        product_depot = Product_Depot.get_product_depot_by_product_id(self.session, product_id)

        stock.quantite += quantity
        if product_depot.quantite_depot - quantity < 0:
            return Exception("Not enough stock in depot to restock the store")
        product_depot.quantite_depot -= quantity
        self.session.commit()

    def get_product_with_stocks(self, store_id):
        products = self.product_repository.get_all_products()
        stocks = []
        for product in products: 
            stock = self.stock_repository.get_stock_by_product_and_store(self.session, product.id, store_id)
            stocks.append(stock)
        return zip(products, stocks)

    def performances(self):
        # Generate the total in sales for each stores, and for each stock of the products in each store, indicates whether the stock is sufficient or not.
        stores = Store.get_all_stores(self.session)
        totals = []
        stocks = []
        store_ids = []
        for store in stores:
            sales = self.sale_repository.get_sales_by_store(store.id)
            total_store = sum(sale.total for sale in sales)
            totals.append(total_store)
            stocks_store = self.stock_repository.get_stock_by_store(self.session, store.id)
            stocks.append(stocks_store)
            store_ids.append(store.id)


        performances_data = zip(totals, stocks, store_ids)
        return performances_data

    def generate_report(self, store_id):
        report = {}
        sales = self.sale_repository.get_sales_by_store(store_id)
        most_sold_product = None
        max_quantity = 0
            
        for sale in sales:
            line_sales = LineSale.get_line_sales_by_sale(self.session, sale.id)
            for line_sale in line_sales:
                if line_sale.quantite > max_quantity:
                    max_quantity = line_sale.quantite
                    most_sold_product = self.product_repository.get_by_id(line_sale.product)

        report["store_id"] = store_id
        report["sales"] = sales
        report["most_sold_product"] = most_sold_product
        report["max_quantity"] = max_quantity

        return report