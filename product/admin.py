from django.contrib import admin
from .models import Product, CartItem

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'for_user_positions')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'for_user_positions')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    search_fields = ('user__email', 'user__name', 'user__phone_no', 'product__name')


admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem, CartItemAdmin)
