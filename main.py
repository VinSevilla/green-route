# Venancio Sevilla 
# GreenRoute carbon emission tracker
# 16 December 2024

import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

def usps_append_location(step_obj, location_list):
    # declared all possible usps sibling tags containing location
    previous_steps = usps_html.find_all(class_="tb-step collapsed")[-1]
    #step = usps_html.select('.tb-step:not(.collapsed):not(.current-step)')
    #current_step = usps_html.find_all(class_="tb-step current-step")[0]
    address = " "  
    # begin at the very first step which is the "tb-step collapsed" class tag 
    # and grab every location upward until we reach step/current step tag
    if step_obj is previous_steps:
        while (step_obj):
            checkpoint_address = step_obj.find(class_="tb-location")
            for words in checkpoint_address:
                address += words.text.strip()
            if address not in location_list:
                location_list.append(address)
            step_obj = step_obj.find_previous_sibling(class_="tb-step collapsed")
        # reset address string
            address = " "
    # grab location directly from their tag
    elif (step_obj is step) or (step_obj is current_step):
        checkpoint_address = step_obj.find(class_="tb-location")
        for words in checkpoint_address:
            address += words.text.strip()
        if address not in location_list:
            location_list.append(address)
    #return location_list
    for checkpoint in location_list:
        print(checkpoint)

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


# Using a try-catch, because sometimes an out of range error occurs 
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
        print("Minimum of 2 destinations have not been detected.")
        
    # if not, get destinations from the first step to the current
    else:
        # 1st step go upwards to each sibling tag until last "tb-step collapsed" class
        previous_steps = usps_html.find_all(class_="tb-step collapsed")[-1]
        # Find only "tb-step" tag
        step = usps_html.select('.tb-step:not(.collapsed):not(.current-step)')
        checkpoints = usps_append_location(previous_steps, checkpoints)
        
        #Most likely the same location regardless, but double check to append just in case
        #checkpoints = usps_append_location(step, checkpoints)
        #checkpoints = usps_append_location(current_step, checkpoints)
        
    for checkpoint in checkpoints:
        print(checkpoint)

except Exception as e:
    print(f"An error occurred: {e}")

# Close the browser
driver.quit()



