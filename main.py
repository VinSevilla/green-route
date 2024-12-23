# Venancio Sevilla 
# GreenRoute carbon emission tracker
# 16 December 2024

from playwright.sync_api import sync_playwright

location_list = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Intercept network requests
    page.on("route", lambda route, request: route.continue_())

    url = "https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1=9200190362719000962473"
    page.goto(url)

    # Wait for the page to load completely
    page.wait_for_load_state("networkidle")

    # Example: Print all package location information
    locations = page.query_selector_all('.tb-location')
    address = " "
    for location in locations:
        address = location.inner_text()
        if address not in location_list:
            location_list.append(address)

    browser.close()

for location in location_list:
    print(location)

