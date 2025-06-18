import pytest
from src.models import User, Sale, LineSale, Product

def test_product():
    product = Product(name="Timbits",category="Snacks",description="Tiny donut balls",prix_unitaire=0.25,stock=100)
    assert product.name == "Timbits"
    assert product.stock == 100
    assert product.prix_unitaire == pytest.approx(0.25)

def test_sale():
    sale = Sale(total=45)
    assert sale.total == 45
    

def test_line_sale():
    line_sale = LineSale(quantite=5, prix=65)
    assert line_sale.quantite == 5
    assert line_sale.prix == 65

def test_user():
    user = User(name="Lojan Arun")
    assert user.name == "Lojan Arun"