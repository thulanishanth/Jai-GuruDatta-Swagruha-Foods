from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch' , 'Lunch'),
        ('Pickles', 'Pickles'),
        ('Snacks', 'Snacks'),
        ('Sweets', 'Sweets'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices= CATEGORY_CHOICES, default='BreakFast')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    
    image = models.ImageField(upload_to='menu/images', blank=True, null=True)
    tag = models.CharField(max_length=20, default='Veg', help_text="e.g. Veg, BestSeller, Spicy")
    
    def __str__(self):
        return self.name
    
    
class Cart(models.Model):
    # OneToOneField means each user has exactly ONE active cart
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
    
    # Helper to calculate total price for this specific item line
    def get_total_price(self):
        return self.quantity * self.menu_item.price