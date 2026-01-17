from django.db import models
from django.conf import settings

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch' , 'Lunch'),
        ('Pickles', 'Pickles'),
        ('Snacks', 'Snacks'),
        ('Sweets', 'Sweets'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices= CATEGORY_CHOICES, default='Breakfast')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    
    image = models.ImageField(upload_to='menu/images', blank=True, null=True)
    tag = models.CharField(max_length=20, default='Veg', help_text="e.g. Veg, BestSeller, Spicy")
    
    def __str__(self):
        return self.name
    
    
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delivered', 'Delivered'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()
        
    def __str__(self):
        return f'{self.quantity} x {self.menu_item.name}'
        
        