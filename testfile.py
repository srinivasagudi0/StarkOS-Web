import requests

# Configuration
API_KEY = "vqpdaJYs1UDwxUET8epRPS0KvS77zfy3Uc7K4Cu_mo"
URL = "https://hackclub.com"

def get_hours_today():
    try:
        # Pass the API key directly as a query parameter
        params = {"api_key": API_KEY}
        response = requests.get(URL, params=params)
        
        # Raise an exception for HTTP errors (4xx, 5xx)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Extract the human-readable text and total seconds
        grand_total = data["data"]["grand_total"]
        time_text = grand_total["text"]              # e.g., "2h 30m"
        total_seconds = grand_total["total_seconds"] # e.g., 9000
        
        # Calculate decimal hours
        decimal_hours = total_seconds / 3600
        
        print(f"Time Spent: {time_text}")
        print(f"Decimal Hours: {decimal_hours:.2f} hrs")
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_hours_today()

