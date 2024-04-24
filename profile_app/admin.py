from django.contrib import admin
from .models import Profile, Product, Cart, CartItem, Order, OrderItem

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
