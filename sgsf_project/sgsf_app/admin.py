from django.contrib import admin
from .models import MenuItem
from .models import MenuItem, Cart, CartItem

# This defines how the list looks in the Admin panel
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'tag')
    list_filter = ('category', 'tag')
    search_fields = ('name', 'description')

# This actually registers it
admin.site.register(MenuItem, MenuItemAdmin)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline] # This lets you see items INSIDE the cart page