from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

class StaticViewSitemap(Sitemap):
    """Sitemap for static views."""
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        # List of view names to include in the sitemap
        return ['gold_view']

    def location(self, item):
        # Generate the URL for each view name
        return reverse(item)

    def lastmod(self, item):
        # Return the last modification time for the item using Django's timezone
        return timezone.now()

# Add other Sitemap classes here if you have models or other views to include
