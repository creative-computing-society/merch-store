from django.contrib import admin
from import_export.resources import ModelResource
from import_export.admin import ExportMixin
from .models import Product, CartItem

# Register your models here.

class ProductResource(ModelResource):
    class Meta:
        model = Product

class ProductAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProductResource

    list_display = ('id', 'name', 'price', 'for_user_positions')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'for_user_positions')


class CartItemResource(ModelResource):
    class Meta:
        model = CartItem

class CartItemAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CartItemResource

    list_display = ('id', 'user', 'product')
    search_fields = ('user__email', 'user__name', 'user__phone_no', 'product__name')


admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem, CartItemAdmin)