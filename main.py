# Venancio Sevilla 
# GreenRoute carbon emission tracker
# 16 December 2024

from playwright.sync_api import sync_playwright
from datetime import datetime
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import re


def carbon_calculation(weight, distance, ef):
    total_carbon_emission = weight * distance * ef
    return total_carbon_emission

def lbs_to_kgs(lbs):
    weight_kg = lbs *  0.453592
    return weight_kg

def clean_time_string(time_str):
    cleaned_time = re.sub(r"Shipping Partner:.*", "", time_str).strip()
    return cleaned_time

def format_seconds(seconds):
    days = seconds // 86400  # There are 86400 seconds in a day
    hours = (seconds % 86400) // 3600  # Get the remaining hours after calculating days (3600 seconds in an hour)
    return int(days), hours

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
    return time_difference.total_seconds() 


geolocator = Nominatim(user_agent="GreenRoute", timeout = 7)

location_list = []
location_date_times = []
location_coordinates = []
# Average emission factors of transportation
avg_delivery_truck_ef = 0.212 # kg
avg_plane_ef = 0.5 # kg

order_number = input("\nEnter or paste USPS order number: ")
while not order_number.isdigit() or len(order_number) < 10:
    order_number = input("\nInvalid input.\nPlease re-enter a valid order number: ")

package_weight_lbs =  int(input("\nEnter weight of item(s). Estimate if needed: "))
while type(package_weight_lbs) != int or package_weight_lbs <= 0:
    package_weight_lbs =  int(input("\nInvalid input.\nPlease re-enter weight: "))

#Convert package lbs to kgs
package_weight = lbs_to_kgs(package_weight_lbs)
 
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page() 

    # Intercept network requests
    page.on("route", lambda route, request: route.continue_())

    url = "https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1=" + order_number
    response = page.goto(url)

    #Validate of URL is accessible
    if response.status == 200:
        print("package data received successfully.\n")
    else:
        print(f"Failed to load the page. Status code: {response.status}")

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

total_co2_emissions = 0
print("")
for i in range(len(location_and_coordinates)-1):
    location1 = location_list[i] # get first location
    coordinates1, time1 = location_and_coordinates[location1]
    location2 = location_list[i+1] # get second location
    coordinates2, time2 = location_and_coordinates[location2]
    time_in_seconds = calculate_time_difference(time2,time1)
    days, hours = format_seconds(time_in_seconds)
    # Calculate the distance between the two locations
    distance = geodesic(coordinates1, coordinates2).kilometers

    # Rough estimate of mode of transportation for emission factor
    speed = distance / (time_in_seconds/3600) # Speed = distance/time(in hours)
    if (distance < 800 and speed <= 120): # likely car conditions used for transportation
        co2_emission = distance * avg_delivery_truck_ef * package_weight
    elif distance >= 800 or speed > 120: #likely plane conditions used for transportation
        co2_emission = distance * avg_plane_ef * package_weight
    total_co2_emissions += co2_emission
    print(f"Distance from {location1} to {location2}: {distance:.2f} km\nTravel time: {days} days, {hours:.1f} hrs.")
    print(f"Estimated CO2 emission: {co2_emission:.2f} CO2e\n\n")

print(f"Total estimated CO2 emissions: {total_co2_emissions:.2f} CO2e\n")
 
