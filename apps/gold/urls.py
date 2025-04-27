from django.urls import path
from . import views

urlpatterns = [
    path('', views.gold_view, name='gold_view'),
    path('api/data/', views.gold_price_data, name='gold_price_data'),
    # Add path for robots.txt - Note: Usually placed at root level in project urls.py
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
