from django.urls import path

from shop.views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('category_list/', CategoryListView.as_view(), name='category-list'),
    path('create_product/', CreateProductView.as_view(), name='create-product'),
    path('create_category/', CreateCategoryView.as_view(), name='create-category'),
    path('update_product/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
    path('update_category/<int:pk>', UpdateCategoryView.as_view(), name='update_category'),
    path('product_detail/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('product_delete/<int:pk>', ProductDeleteView, name='product-delete'),
    path('category_delete/<int:pk>', CategoryDeleteView, name='category-delete'),
    path('my_products/', MyProductsView, name='my-products'),

    path('shopping_basket/',ShoppingBasket, name='shopping_basket'),
    path('add_shopping_basket/<int:pk>', AddShoppingBasket, name='add_shopping_basket'),
    path('delete_shopping_basket/<int:pk>', delete_from_basket, name='delete_shopping_basket'),

    path('owners/',Owners.as_view(), name='owners'),
    path('owner/<int:pk>', Owner, name='owner'),

    path('error1/',Error1.as_view(), name='error1'),
    path('error2/',Error2.as_view(), name='error2'),

    path('placing_an_order/<int:pk>', placing_an_order, name='placing_an_order'),
    path('orders/', Orders.as_view(), name='order_list'),
    path('order/<int:pk>', OrderDetail.as_view(), name='order_detail'),
]