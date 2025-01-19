from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('complete/', views.complete_order, name='complete_order'),
    path('complete-order/<int:order_id>/', views.complete_order_view, name='complete_order'),
    path('generate-end-of-day-report/', views.generate_end_of_day_report, name='generate_end_of_day_report'),
   
]
