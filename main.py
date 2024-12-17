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

# give time for page to load
time.sleep(5)

# Get the page source after JavaScript has loaded
html = driver.page_source

# Parse the HTML with BeautifulSoup
usps_html = BeautifulSoup(html, 'html.parser')

shipping_address = ""
destination = ""

# Because the webpage is dynamic, check shipping status of current step html element 
current_step = usps_html.find_all(class_="tb-step current-step")[0]
# get the shipping status from the html current step
shipping_status = current_step.find_all(class_="tb-status-detail")
# parcel the shipping status into a single string
status = ""
for words in shipping_status:
    status += words.text.strip()

#if the current step is the origin shipping label address
if status == "Shipping Label Created, USPS Awaiting Item":
    original_address = current_step.find_next_siblings(class_="tb-location")

# if not, get it from the very 1st step of the delivery progress
else:
    first_step = usps_html.find_all(class_="tb-step collapsed")[-1]
    original_address = first_step.find(class_="tb-location")

for words in original_address:
    shipping_address += words.text.strip()

print(shipping_address)

# Close the browser
driver.quit()

#fix github push contributions
print("test contributions")

