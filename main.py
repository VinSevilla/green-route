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
address = " "
checkpoints = []

try:
    # Because the webpage is dynamic, check shipping status of current step html element 
    current_step = usps_html.find_all(class_="tb-step current-step")[0]
    # get the shipping status from the html current step
    shipping_status = current_step.find_all(class_="tb-status-detail")
    # parcel the shipping status into a single string
    status = " "
    for words in shipping_status:
        status += words.text.strip()
    #if the current step is the origin shipping label address
    if status == "Shipping Label Created, USPS Awaiting Item":
        shipping_address = current_step.find_next_siblings(class_="tb-location")
        for words in shipping_address:
            address += words.text.strip()
        
    # if not, get destinations from the first step to the current
    else:
        # 1st step
        step = usps_html.find_all(class_="tb-step collapsed")[-1]
        while (step):
            # reset address string
            address = " "
            checkpoint_address = step.find(class_="tb-location")
            for words in checkpoint_address:
                address += words.text.strip()
            if address not in checkpoints:
                checkpoints.append(address)
            step = step.find_previous_sibling(class_="tb-step collapsed")
            
    for checkpoint in checkpoints:
        print(checkpoint)
except Exception as e:
    print(f"An error occurred: {e}")

# Close the browser
driver.quit()



