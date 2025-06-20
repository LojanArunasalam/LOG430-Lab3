from django.urls import path
from . import product_views, sale_views, domain_views

urlpatterns = [
    # Products routes
    path('api/v1/products', product_views.get_all_products),
    path('api/v1/products/<int:id>/', product_views.get_product_by_id),
    path('api/v1/products/category/<str:category>/', product_views.product_by_category),
    path('api/v1/products/add/', product_views.add_product),
    path('api/v1/products/del/<int:id>', product_views.delete_product),

    # Sales routes
    # Stock routes
    # Product_Depot routes
    # LineSales routes
    # Stores routes

    # Performances routes
    path('api/v1/performances/', domain_views.performances),
    # Report routes
    path('api/v1/report/<int:store_id>', domain_views.report)

]
