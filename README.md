# GreenRoute: Carbon Emission Tracker for Shipping Logistics

## Overview

**GreenRoute** is a carbon emission tracking tool designed to estimate the environmental impact of shipping packages based on their travel distance, time, and transportation method. The tool collects tracking information for USPS packages, calculates travel times between locations, estimates the transportation mode (truck or airplane), and computes the corresponding carbon emissions. This tool helps raise awareness of the carbon footprint of logistics operations and enables users to make more informed decisions about their shipping methods.

## Features

- **Track Packages**: Users can input a USPS order number to track their package and retrieve location updates.
- **CO2 Emission Calculation**: Estimates the carbon emissions based on package weight, distance, and transport method (truck or airplane).
- **Distance Calculation**: Uses geographic coordinates to calculate the distance between package delivery locations.
- **Mode of Transportation Estimate**: Determines if the package was likely transported by truck or plane based on travel speed and distance.
- **Time Difference**: Calculates travel time between locations and formats it into days and hours.

## Requirements

To run this project, the following Python libraries are required:

- `playwright`: For web scraping USPS tracking data.
- `geopy`: For geolocation services and distance calculation.
- `re`: For regex-based text cleaning.

You can install the required libraries with pip:

```bash
pip install playwright geopy
```
## How It Works
- **Package Tracking**: The user enters a USPS order number. The program fetches tracking data from the USPS tracking page.
- **Location and Time Extraction**: The program extracts all delivery locations and timestamps from the tracking data.
- **Distance Calculation**: It calculates the distance between two consecutive delivery locations using their geographic coordinates.
- **Emission Factor Estimation**: The program estimates the transportation mode (truck or plane) based on distance and travel time, using the average carbon emission factors for trucks and planes.
- **CO2 Emission Calculation**: The program calculates the total CO2 emissions for each leg of the journey and aggregates them to provide a total CO2 emission estimate for the package’s journey.

## How It Works
- Run the script.
When prompted, enter the USPS tracking number.
The script will display:
1. The distance and travel time between each consecutive delivery location.
2. The estimated CO2 emissions for each leg of the journey.
3. The total estimated CO2 emissions for the entire package journey.

## Notes
- **Transportation Mode**: The script estimates the mode of transportation based on distance and speed. If the distance is less than 800 km and the speed is under 120 km/h, the program assumes a delivery truck was used. For longer distances or higher speeds, it assumes an airplane was used.
- **CO2 Emission Factors**: The average emission factors for delivery trucks (0.212 kg CO2 per ton-mile) and airplanes (0.5 kg CO2 per ton-kilometer) are used in the calculations.


