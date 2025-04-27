from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils.feedgenerator import Rss201rev2Feed
from .views import get_latest_gold_data # Import the helper function
from django.utils import timezone
from datetime import datetime

class CorrectMimeTypeFeed(Rss201rev2Feed):
    """
    Create a subclass of the Feed class
    that sets the correct MIME type.
    """
    mime_type = 'application/xml' # Use application/xml for RSS

class LatestGoldPriceFeed(Feed):
    """
    An RSS feed for the latest gold price update.
    """
    feed_type = CorrectMimeTypeFeed
    title = "Harga Emas Indonesia Terbaru (IDR per 0.01g)"
    link = reverse_lazy('gold_view') # Link to the main gold page
    description = "Update harga jual dan beli emas terbaru di Indonesia dalam Rupiah (IDR) per 0.01 gram."
    description_template = 'feeds/latest_gold_description.html' # Optional: Template for item description

    def items(self):
        """
        Returns a list containing only the latest gold data entry,
        or an empty list if no data is available.
        """
        latest_data = get_latest_gold_data()
        return [latest_data] if latest_data else []

    def item_title(self, item):
        """Returns the title for a single feed item."""
        if item and item.get('parsedUpdate'):
            # Format date like "Update Harga Emas: 01 Jan 2024 10:30"
            formatted_date = item['parsedUpdate'].strftime('%d %b %Y %H:%M')
            return f"Update Harga Emas: {formatted_date}"
        return "Update Harga Emas Terbaru"

    def item_description(self, item):
        """Returns the description for a single feed item."""
        if item:
            sell_price = item.get('hargaJual', 'N/A')
            buy_price = item.get('hargaBeli', 'N/A')
            # Format prices with IDR
            try:
                sell_price_formatted = f"Rp{int(sell_price):,}".replace(',', '.')
            except (ValueError, TypeError):
                sell_price_formatted = "N/A"
            try:
                buy_price_formatted = f"Rp{int(buy_price):,}".replace(',', '.')
            except (ValueError, TypeError):
                buy_price_formatted = "N/A"

            return f"Harga Jual: {sell_price_formatted}, Harga Beli: {buy_price_formatted} (per 0.01g)"
        return "Data harga emas tidak tersedia."

    def item_link(self, item):
        """Returns the link for a single feed item (links back to the main page)."""
        return self.link # Link item back to the main gold view page

    def item_pubdate(self, item):
        """Returns the publication date for a single feed item."""
        if item and item.get('parsedUpdate'):
            # Ensure the datetime is timezone-aware (use project's timezone)
            dt_aware = timezone.make_aware(item['parsedUpdate'], timezone.get_current_timezone())
            return dt_aware
        return timezone.now() # Fallback to current time
