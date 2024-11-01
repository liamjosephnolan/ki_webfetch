from apscheduler.schedulers.blocking import BlockingSchedulerimport
import time
import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime 

# URL of the page to scrape
url = 'https://www.kletterzentrum-innsbruck.at/'

# Start the timer
start_time = time.time()

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

    # Find the span with the class 'ki-entry-pct'
    ki_current_capacity = website_soup.find('span', class_='ki-entry-pct')


    # Extract the text and convert it to an integer if the element is found
    if ki_current_capacity:
        try:
            ki_current_capacity = int(ki_current_capacity.get_text())
            print("The extracted number is:", ki_current_capacity)
        except:
            ki_current_capacity = 0
    else:
        print("The element with class 'ki-entry-pct' was not found.")
        ki_current_capacity = 0


csv_file = 'ki_current_capacity_log.csv'

current_time = datetime.now() # get current time

# Append data to the CSV file
with open(csv_file, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([current_time, ki_current_capacity])  



# Stop the timer and calculate the elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken to fetch and parse the content: {elapsed_time:.2f} seconds")



# Create a scheduler
scheduler = BlockingScheduler()
# Schedule the fetch_data function to run every 10 minutes
scheduler.add_job(fetch_data, 'interval', minutes=10)

# Start the scheduler
scheduler.start()
