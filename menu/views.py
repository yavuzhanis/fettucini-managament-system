from django.shortcuts import render
from menu.models import *
# Create your views here.
def menu_view(request):
    food_items = FoodItem.objects.all()
    drink_items = DrinkItem.objects.all()
    return render(request, 'index.html', {'food_items': food_items, 'drink_items': drink_items})