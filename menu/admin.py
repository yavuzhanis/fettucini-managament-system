from django.contrib import admin
from .models import FoodItem, DrinkItem

class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'small_price', 'medium_price')  # small_price ve medium_price alanlarını ekleyin
    search_fields = ('name',)  # Arama yapmak için 'name' alanını ekledik
    list_filter = ('small_price', 'medium_price')  # Fiyat alanlarına göre filtreleme yapılacak

class DrinkItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'small_price', 'medium_price')  # small_price ve medium_price alanlarını ekleyin
    search_fields = ('name',)  # Arama yapmak için 'name' alanını ekledik
    list_filter = ('small_price', 'medium_price')  # Fiyat alanlarına göre filtreleme yapılacak

# Modelleri admin paneline kaydediyoruz
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(DrinkItem, DrinkItemAdmin)
