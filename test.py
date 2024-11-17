import requests



# Url for weather in Innsbruck 
weather_url = 'https://api.open-meteo.com/v1/forecast?latitude=47.27001&longitude=11.39577&current_weather=true'
weather_response = requests.get(weather_url)  # Get response from Open Meteo API
current_weather_data = weather_response.json()  # Convert the response to JSON

# Parse weather data from Open Meteo's response
current_temp = current_weather_data['current_weather']['temperature']
weather_code = current_weather_data['current_weather']['weathercode']

print(current_temp)
print(weather_code)

