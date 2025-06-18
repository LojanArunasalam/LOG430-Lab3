from django.shortcuts import render, HttpResponse, redirect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from .models import Product, Stock, Sale, LineSale, Store, Product_Depot, engine, logging
from . import controller
from .caisse_controller import Caisse

Session = sessionmaker(bind=engine)
session = Session()

def home(request):
    logging.info("Rendering home page")
    return render(request, "home.html")

def report(request, store_id):
    logging.info(f"Rendering report for store {store_id}")
    return render(request, "report.html", controller.generate_report(store_id))

def restock_product(request, product_id, store_id):
    logging.info(f"Restocking...")
    quantity = 1 
    # r_product_id = request.GET.get('product_id')
    # r_store_id = request.GET.get('store_id')

    controller.restock_from_depot(product_id, quantity, store_id)
    return redirect("products")  # Redirect back to products page

def performances(request):
    logging.info("Rendering performances page")
    performances_data = controller.performances()
    return render(request, "performances.html", {
        "performances" : performances_data
    })

def search_products(request):
    logging.info("Rendering search products page")
    r_id = request.GET.get('id')

    if not r_id: 
        zipped1 = controller.get_product_with_stocks(1)
        zipped2 = controller.get_product_with_stocks(2)
        zipped3 = controller.get_product_with_stocks(3)
        zipped4 = controller.get_product_with_stocks(4)
        zipped5 = controller.get_product_with_stocks(5)

        return render(request, "products.html", {
            "zipped1": zipped1,
            "zipped2": zipped2,
            "zipped3": zipped3,
            "zipped4": zipped4,
            "zipped5": zipped5
        })
    else: 
        product = Product.get_by_id(session, r_id)

        if not product: 
            return HttpResponse("Product not found")
        
        zipped1 = zip([product], [Stock.get_stock_by_product_and_store(session, product.id, 1)])
        zipped2 = zip([product], [Stock.get_stock_by_product_and_store(session, product.id, 2)])
        zipped3 = zip([product], [Stock.get_stock_by_product_and_store(session, product.id, 3)])
        zipped4 = zip([product], [Stock.get_stock_by_product_and_store(session, product.id, 4)])
        zipped5 = zip([product], [Stock.get_stock_by_product_and_store(session, product.id, 5)])

        return render(request, "products.html", 
            { 
                "zipped1": zipped1,
                "zipped2": zipped2,
                "zipped3": zipped3,
                "zipped4": zipped4,
                "zipped5": zipped5
            })

def dashboard_logistique(request):
    logging.info("Rendering stock-central page")
    depots = Product_Depot.get_all_product_depots(session)
    return render(request, "stock-central.html", {"depots": depots})


def buy_product(request, product_id, store_id):
    caisse = Caisse(store_id)
    caisse.enregistrer_vente(product_id)
    return redirect("products")



