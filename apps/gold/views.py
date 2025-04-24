import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.conf import settings
from datetime import datetime, date, timedelta # Import date, timedelta
from dateutil.relativedelta import relativedelta # Import relativedelta

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
    Fetch gold price data from the external API, filter by a calculated date range based on 'period',
    and return the filtered data as JSON.
    """
    period_str = request.GET.get('period', '1m') # Default to 1 month
    today = date.today()
    start_date = today # Default start date

    # Calculate start_date based on period
    try:
        if period_str.endswith('d'):
            days = int(period_str[:-1])
            start_date = today - timedelta(days=days)
        elif period_str.endswith('m'):
            months = int(period_str[:-1])
            start_date = today - relativedelta(months=months)
        elif period_str.endswith('y'):
            years = int(period_str[:-1])
            start_date = today - relativedelta(years=years)
    except ValueError:
        # Handle invalid period format, maybe default or return error
        period_str = '1m' # Fallback to 1 month
        start_date = today - relativedelta(months=1)

    # Fetch data using a large interval to cover the maximum possible range (e.g., 20 years)
    # Adjust MAX_INTERVAL_DAYS based on the maximum period offered (e.g., 20y = ~7300 days)
    MAX_INTERVAL_DAYS = 7305 # A bit over 20 years to be safe
    url = f"{settings.DATA_URL}?interval={MAX_INTERVAL_DAYS}&isRequest=true"

    try:
        response = requests.get(url, timeout=20) # Increased timeout for potentially larger response
        response.raise_for_status()
        data = response.json()

        # Extract data portion if response is successful
        if data.get("responseCode") == "2000000100" and "data" in data and "priceList" in data["data"]:
            price_list = data["data"]["priceList"]

            # Filter the priceList based on the calculated date range
            filtered_price_list = []
            start_datetime = datetime.combine(start_date, datetime.min.time()) # Convert start_date to datetime

            for item in price_list:
                try:
                    item_date = datetime.strptime(item.get('lastUpdate', ''), '%Y-%m-%d %H:%M:%S')
                    # Include data from start_date up to the current moment
                    if item_date >= start_datetime:
                         filtered_price_list.append(item)
                except (ValueError, TypeError):
                    continue # Skip items with invalid date format

            # Return the filtered data
            return JsonResponse({"priceList": filtered_price_list}) # Match original structure if needed
        else:
            return JsonResponse({
                "error": "No data available or API error",
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
