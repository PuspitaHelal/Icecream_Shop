from django.contrib import admin
from .models import IceCream, CartItem, Order, OrderItem

# Register models so they appear in admin
admin.site.register(IceCream)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)