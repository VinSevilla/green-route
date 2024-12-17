# Venancio Sevilla 
# GreenRoute carbon emission tracker
# 16 December 2024
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
# URL of package
url = "https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1=9200190362719000962473"


# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(options=options)

# Open the URL
driver.get(url)
time.sleep(5)
# Get the page source after JavaScript has loaded
html = driver.page_source



# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find and print locations
shipping_address = soup.find_all(class_="tb-location")
for location in shipping_address:
    print(location.text.strip())

# Close the browser
driver.quit()


