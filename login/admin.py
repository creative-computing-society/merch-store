from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'position', 'phone_no')
    list_display_links = ('id', 'email')
    list_filter = ('position', )
    search_fields = ('email', 'name', 'phone_no')

admin.site.register(User, UserAdmin)
