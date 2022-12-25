from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'user', 'items_count')
    search_fields = ('id', 'user_email')

    def items_count(self, obj):
        return (obj.products.count())


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'printing_name', 'size')
    search_fields = ('product__name', 'order__id', 'order__user__email')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
