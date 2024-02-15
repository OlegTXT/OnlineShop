from django.contrib import admin

from shop.models import Category, Product, ShopBasket, Order

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ShopBasket)
admin.site.register(Order)
