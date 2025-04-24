import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.conf import settings
from datetime import datetime # Import datetime

def get_latest_gold_data():
    """
    Helper function to fetch the latest gold price data.
    Returns the latest price entry or None if an error occurs.
    """
    # Use a default interval likely to contain the latest price list
    url = f"{settings.DATA_URL}?interval=1&isRequest=true"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Check if data and priceList exist and are not empty
        if data.get("responseCode") == "2000000100" and data.get("data", {}).get("priceList"):
            latest_data = data["data"]["priceList"][0]
            # Attempt to parse the date string
            try:
                latest_data['parsedUpdate'] = datetime.strptime(latest_data['lastUpdate'], '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                latest_data['parsedUpdate'] = None # Handle parsing error
            return latest_data
        else:
            # Log error: Invalid data structure or non-success response code
            print(f"API Error or unexpected structure: {data.get('responseDesc', 'No description')}")
            return None
    except requests.RequestException as e:
        # Log error: Request failed
        print(f"Error fetching latest gold data: {e}")
        return None
    except (json.JSONDecodeError, IndexError, KeyError) as e:
         # Log error: JSON parsing or data access error
        print(f"Error processing gold data response: {e}")
        return None


def gold_view(request):
    """
    Render the gold price tracker page and include latest data for JSON-LD.
    """
    latest_gold_data = get_latest_gold_data()
    context = {
        'latest_gold_data': latest_gold_data
    }
    return render(request, 'gold/gold.html', context)

@cache_page(60 * 5)  # Cache the response for 5 minutes
def gold_price_data(request):
    """
    Fetch gold price data from the external API and return only the data portion as JSON.
    """
    interval = request.GET.get('interval', '1')

    url = f"{settings.DATA_URL}?interval={interval}&isRequest=true"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract only the data portion if response is successful
        if data.get("responseCode") == "2000000100" and "data" in data:
            return JsonResponse(data["data"])
        else:
            return JsonResponse({
                "error": "No data available",
                "message": data.get("responseDesc", "Unknown error")
            }, status=404)
            
    except requests.RequestException as e:
        return JsonResponse({
            "error": "Error fetching data",
            "message": str(e)
        }, status=500)
    except json.JSONDecodeError:
         return JsonResponse({
            "error": "Error decoding API response",
            "message": "Invalid JSON received from external API"
        }, status=500)
