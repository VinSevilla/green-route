# Venancio Sevilla 
# GreenRoute carbon emission tracker
# 16 December 2024

from playwright.sync_api import sync_playwright

from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def carbon_calculation(weight, disance, ef):
    total_carbon_emission = weight * distance * ef
    return total_carbon_emission

geolocator = Nominatim(user_agent="GreenRoute", timeout = 5)

location_list = []
location_coordinates = []
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
    address = " "
    for location in locations:
        address = location.inner_text().strip()
        if address != '' and address not in location_list:
            location_list.append(address)

    browser.close()

# Find coordinates for each location in location_list
for location in location_list:
    coordinates = geolocator.geocode(location)
    if coordinates:
        lat_long = (coordinates.latitude, coordinates.longitude)
        location_coordinates.append(lat_long)
    else:
        location_coordinates.append("Not Found.")


location_and_coordinates = {key:value for key, value in zip(location_list,location_coordinates)}
print(location_and_coordinates)
