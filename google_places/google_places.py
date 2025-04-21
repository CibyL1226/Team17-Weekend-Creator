import requests
import json
import time

API_KEY = ""

cities = [
    ("Oklahoma City", "Oklahoma"), ("Saint Louis", "Missouri"), ("Indianapolis", "Indiana"),
    ("Spokane", "Washington"), ("Des Moines", "Iowa"), ("Port Saint Lucie", "Florida"),
    ("Salt Lake City", "Utah"), ("Arlington", "Texas"), ("Costa Mesa", "California"),
    ("Inglewood", "California"), ("Omaha", "Nebraska"), ("Miami", "Florida"),
    ("Boston", "Massachusetts"), ("Tampa", "Florida"), ("Philadelphia", "Pennsylvania"),
    ("Atlanta", "Georgia"), ("Sunrise", "Florida"), ("New Orleans", "Louisiana"),
    ("Lexington", "Kentucky"), ("Warren", "Michigan"), ("San Diego", "California"),
    ("East Lansing", "Michigan"), ("Chicago", "Illinois"), ("Detroit", "Michigan"),
    ("Anaheim", "California"), ("Pittsburgh", "Pennsylvania"), ("Newark", "New Jersey"),
    ("Saint Paul", "Minnesota"), ("Brooklyn", "New York"), ("New York", "New York"),
    ("Portland", "Oregon"), ("Loveland", "Colorado"), ("Las Vegas", "Nevada"),
    ("Austin", "Texas"), ("Primm", "Nevada"), ("Rockford", "Illinois"),
    ("Houston", "Texas"), ("Ontario", "California"), ("Lakeland", "Florida"),
    ("Bakersfield", "California"), ("Cleveland", "Ohio"), ("Atlantic City", "New Jersey"),
    ("Phoenix", "Arizona"), ("Seattle", "Washington"), ("East Rutherford", "New Jersey"),
    ("Kansas City", "Missouri"), ("Cincinnati", "Ohio"), ("Missoula", "Montana"),
    ("Denver", "Colorado"), ("Bronx", "New York"), ("Buffalo", "New York"),
    ("Washington", "District of Columbia"), ("San Antonio", "Texas"), ("Los Angeles", "California"),
    ("Eugene", "Oregon"), ("Tucson", "Arizona"), ("Augusta", "Georgia"),
    ("Chattanooga", "Tennessee"), ("Baltimore", "Maryland"), ("West Sacramento", "California"),
    ("Staten Island", "New York"), ("Flushing", "New York")
]

PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

def get_restaurants(city, max_results=60):
    url = PLACES_URL
    restaurants = []
    next_page_token = None
    
    while len(restaurants) < max_results:
        params = {
            "query": f"restaurants in {city}",
            "key": API_KEY,
        }
        if next_page_token:
            params["pagetoken"] = next_page_token
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if "results" in data:
            for place in data["results"]:
                place_id = place.get("place_id")
                details = get_place_details(place_id)

                restaurant = {
                    "place_id": place_id,
                    "name": details.get("name"),
                    "address": details.get("formatted_address"),
                    "rating": details.get("rating"),
                    "price_level": details.get("price_level"),
                    "types": details.get("types"),
                    "coordinates": details.get("geometry", {}).get("location"),
                    "website": details.get("website"),
                    "phone_number": details.get("formatted_phone_number"),
                    "opening_hours": details.get("opening_hours"),
                    "reviews": details.get("reviews"),
                    "photos": details.get("photos"),
                    "google_maps_url": details.get("url"),
                }
                restaurants.append(restaurant)
                
                if len(restaurants) >= max_results:
                    break
        
        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break
        
        time.sleep(2)  
    
    return restaurants

def get_place_details(place_id):
    params = {
        "place_id": place_id,
        "key": API_KEY,
        "fields": "name,formatted_address,formatted_phone_number,website,opening_hours,reviews,photos,url,geometry,price_level,rating,types"
    }
    response = requests.get(DETAILS_URL, params=params)
    return response.json().get("result", {})

def save_to_json(city, data):
    with open(f"{city}_restaurants.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

for city, state in cities:
    city_name = f"{city}, {state}"
    print(f"Fetching data for {city_name}...")
    restaurants_data = get_restaurants(city_name)
    save_to_json(city_name, restaurants_data)
    print(f"Data for {city_name} saved.")