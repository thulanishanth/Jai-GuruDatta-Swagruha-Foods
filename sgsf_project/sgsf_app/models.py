from django.db import models

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
    