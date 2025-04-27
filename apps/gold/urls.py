from django.urls import path
from . import views
from .feeds import LatestGoldPriceFeed # Import the feed class

urlpatterns = [
    path('', views.gold_view, name='gold_view'),
    path('api/data/', views.gold_price_data, name='gold_price_data'),
    # Add path for robots.txt - Note: Usually placed at root level in project urls.py
    path('robots.txt', views.robots_txt, name='robots_txt'),
    # Add path for the RSS feed
    path('feed/', LatestGoldPriceFeed(), name='latest_gold_feed'), # View name is 'latest_gold_feed'
]
