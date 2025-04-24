from django.urls import path
from . import views

urlpatterns = [
    path('', views.gold_view, name='gold_view'),
    path('api/data/', views.gold_price_data, name='gold_price_data'),
]
