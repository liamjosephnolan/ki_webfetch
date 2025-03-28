import time
import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime 


def get_weather_description(weather_code):
    # Dictionary mapping weather codes to descriptions
    weather_descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Slight or moderate thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    # Get the weather description based on the code
    return weather_descriptions.get(weather_code, "Unknown weather condition")


# URL of the page to scrape
url = 'https://www.kletterzentrum-innsbruck.at/'

requests.get('https://ki-webfetch.onrender.com/api/average_capacity') #Only have this to keep my render service online

# Weather data code
try: # Blanket try case
    # Url for weather in Innsbruck 
    weather_url = 'https://api.open-meteo.com/v1/forecast?latitude=47.27001&longitude=11.39577&current_weather=true'
    weather_response = requests.get(weather_url)  # Get response from Open Meteo API
    current_weather_data = weather_response.json()  # Convert the response to JSON

    # Parse weather data from Open Meteo's response
    current_temp = current_weather_data['current_weather']['temperature']
    weather_code = current_weather_data['current_weather']['weathercode']
    current_weather_type = get_weather_description(weather_code)
except:
    current_weather_type = None
    current_temp = None

# Fetch the webpage content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Print the HTML content of the page.
    html_content = response.text
    print("Content Fetched")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    html_content = ""

# Create a BeautifulSoup object only if content was fetched
if html_content:
    website_soup = BeautifulSoup(html_content, 'html.parser')

    # Find the span with the class 'opening-hours-conditional'
    capacity_span = website_soup.find('span', class_='opening-hours-conditional')
    
    # If not found with the exact class, try finding with partial class match
    if not capacity_span:
        capacity_span = website_soup.find('span', class_=lambda x: x and 'opening-hours-conditional' in x)

    # Extract the capacity percentage if the element is found
    if capacity_span:
        try:
            capacity_text = capacity_span.get_text().strip()
            # Remove the percentage sign and convert to integer
            ki_current_capacity = int(capacity_text.replace('%', ''))
            print("The extracted capacity is:", ki_current_capacity)
        except (AttributeError, ValueError) as e:
            print(f"Error extracting capacity: {e}")
            ki_current_capacity = 0
    else:
        print("The capacity element was not found.")
        ki_current_capacity = 0


csv_file = 'ki_current_capacity_log.csv'

current_time = datetime.now() # get current time

# Append data to the CSV file
with open(csv_file, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([current_time, ki_current_capacity, current_temp, current_weather_type])