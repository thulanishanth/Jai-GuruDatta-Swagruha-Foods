from django.contrib import admin
from .models import MenuItem

# This defines how the list looks in the Admin panel
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'tag')
    list_filter = ('category', 'tag')
    search_fields = ('name', 'description')

# This actually registers it
admin.site.register(MenuItem, MenuItemAdmin)