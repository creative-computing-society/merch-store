from django.contrib import admin
from .models import DiscountCode

class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percentage', 'max_uses', 'expiry_date', 'custom']
    list_filter = ['custom']
    search_fields = ['code']

    fieldsets = (
        (None, {
            'fields': ('code', 'discount_percentage', 'max_uses', 'expiry_date', 'for_user_positions', 'custom')
        }),
    )

admin.site.register(DiscountCode, DiscountCodeAdmin)
