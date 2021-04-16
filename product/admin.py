from django.contrib import admin
from .models import Category, Product, Order, OrderProduct

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
