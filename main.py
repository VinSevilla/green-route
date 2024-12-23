# Venancio Sevilla 
# GreenRoute carbon emission tracker
# 16 December 2024

from playwright.sync_api import sync_playwright
from datetime import datetime
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import re

def carbon_calculation(weight, distance, ef):
    total_carbon_emission = weight * distance * ef
    return total_carbon_emission

def clean_time_string(time_str):
    cleaned_time = re.sub(r"Shipping Partner:.*", "", time_str).strip()
    return cleaned_time

def calculate_time_difference(time1_str, time2_str):
    # Define the format of the time strings (adjust if the format changes)
    time_format = "%B %d, %Y, %I:%M %p"  

    #clean time formatting
    time1_str = clean_time_string(time1_str)
    time2_str = clean_time_string(time2_str)

    # Convert time strings to datetime objects
    time1 = datetime.strptime(time1_str, time_format)
    time2 = datetime.strptime(time2_str, time_format)

    # Calculate the difference
    time_difference = time2 - time1

    # Return the difference in total seconds (can be adjusted to minutes, hours, etc.)
    return time_difference.total_seconds() / 3600 # convert to hours

geolocator = Nominatim(user_agent="GreenRoute", timeout = 7)

location_list = []
location_date_times = []
location_coordinates = []
avg_delivery_truck_er = 0.212 # 0.212g per ton-mile
avg_plane_er = 500 # 500g ton-kilo
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Intercept network requests
    page.on("route", lambda route, request: route.continue_())

    url = "https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1=9200190362719000962473"
    page.goto(url)

    # Wait for the page to load completely
    page.wait_for_load_state("networkidle")

    # find all locations within html code
    locations = page.query_selector_all('.tb-location')
    date_times = page.query_selector_all('.tb-date')
    address = " "
    for i in range(len(locations)):
        address = locations[i].inner_text().strip()
        time = date_times[i].inner_text().strip()
        # Only add the first occurrence of each location with the associated time
        if address != '' and address not in location_list:
            location_list.append(address)
            location_date_times.append(time)
    browser.close()

# Find coordinates for each location in location_list
for location in location_list:
    coordinates = geolocator.geocode(location)
    if coordinates:
        lat_long = (coordinates.latitude, coordinates.longitude)
        location_coordinates.append(lat_long)
    else:
        location_coordinates.append("Not Found.")

# pair values of coordinates with locations
location_and_coordinates = {key:(val1,val2) for key, val1, val2 in zip(location_list,location_coordinates,location_date_times)}

for i in range(len(location_and_coordinates)-1):
    location1 = location_list[i] # get first location
    coordinates1, time1 = location_and_coordinates[location1]
    location2 = location_list[i+1] # get second location
    coordinates2, time2 = location_and_coordinates[location2]
    total_time = calculate_time_difference(time2,time1)

    
    # Calculate the distance between the two locations
    distance = geodesic(coordinates1, coordinates2).kilometers
    print(f"Distance from {location1} to {location2}: {distance:.2f} km\nTravel time: {total_time:.2f}\n\n")
