from django.db import models

# Models
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    small_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    medium_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name

class DrinkItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='drink_images/', blank=True, null=True)
    small_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    medium_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name