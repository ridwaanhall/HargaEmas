import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

def gold_view(request):
    """
    Render the gold price tracker page.
    """
    return render(request, 'gold/gold.html')

@cache_page(60 * 5)  # Cache the response for 5 minutes
def gold_price_data(request):
    """
    Fetch gold price data from the external API and return as JSON.
    """
    interval = request.GET.get('interval', '7')
    
    # Make request to external API
    url = f"https://sahabat.pegadaian.co.id/gold/prices/chart?interval={interval}&isRequest=true"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return JsonResponse(data)
    except requests.RequestException as e:
        return JsonResponse({
            "responseCode": "5000000100",
            "responseDesc": "Error fetching data",
            "message": str(e)
        }, status=500)
