from .models import Product, Stock, Sale, LineSale, Store, User, Product_Depot, engine
from sqlalchemy.orm import sessionmaker
import logging

Session = sessionmaker(bind=engine)
session = Session()

class Caisse:
    def __init__(self, store_id):
        self.store_id = store_id
        
    def enregistrer_vente(self, product_id):
        lignes_ventes = []
        product = Product.get_by_id(session, product_id)
        stock = Stock.get_stock_by_product_and_store(session, product.id, self.store_id)

        
        if stock.quantite - 1 < 0:
            return Exception("Stock insuffisant pour ce produit")
                    
        self.update_stock(product_id, 1)
        session.add(stock)
        session.commit()
        ligne_vente = self.enregistrer_ligne_vente(product_id, 1)
        lignes_ventes.append(ligne_vente)

        total = 0
        for line in lignes_ventes:
            total = total + line.prix
            session.add(line)

        sale = Sale(total=total, store=self.store_id)
        sale.line_vente.extend(lignes_ventes)

        session.add(sale)
        session.commit()

    def enregistrer_ligne_vente(self, product_id, quantite):
        product = Product.get_by_id(session, product_id)
        ligne_vente = LineSale(product=product_id, quantite=quantite, prix=product.prix_unitaire)
        return ligne_vente
        

    def update_stock(self, product_id, quantite):
        stock = Stock.get_stock_by_product_and_store(session, product_id, self.store_id)
        stock.quantite -= quantite
        session.add(stock)
        session.commit()
