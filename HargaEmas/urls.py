"""
URL configuration for HargaEmas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap # Import sitemap view
from apps.gold.sitemaps import StaticViewSitemap # Import your sitemap class
# Import the robots.txt view if you want to move its URL pattern here (recommended)
# from apps.gold import views as gold_views

# Define the sitemaps dictionary
sitemaps = {
    'static': StaticViewSitemap,
    # Add other sitemaps here if needed
}

urlpatterns = [
    path('', include('apps.gold.urls')), # Assuming gold app is at the root or adjust prefix
    # Add the sitemap URL pattern at the root
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Optional but recommended: Move robots.txt path here from apps.gold.urls
    # path('robots.txt', gold_views.robots_txt),

    # ... other project urls
]

# Note: If you move the robots.txt path here, remove it from apps/gold/urls.py
# and update the robots_txt view in apps/gold/views.py to use
# reverse('django.contrib.sitemaps.views.sitemap') again, as the sitemap URL will now be defined.
