from django.contrib import admin
from import_export.resources import ModelResource
from import_export.admin import ExportMixin
from .models import Order, OrderItem

# Register your models here.

class OrderResource(ModelResource):
    class Meta:
        model = Order

class OrderAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderResource

    list_display = ('id', 'user', 'updated_amount', 'is_verified', 'items_count')
    search_fields = ('id', 'user__email')
    list_filter = ('is_verified', )
    list_editable = ('is_verified', )
    exclude = ('cart_restored', )

    def items_count(self, obj):
        return obj.order_items.count()

class OrderItemResource(ModelResource):
    class Meta:
        model = OrderItem

class OrderItemAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderItemResource

    list_display = ('id', 'order', 'product', 'printing_name', 'size', 'image_url')
    search_fields = ('product__name', 'order__id', 'order__user__email')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
