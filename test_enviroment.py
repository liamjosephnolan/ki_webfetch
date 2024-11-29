import pandas as pd



csv_file = 'ki_current_capacity_log.csv'


df = pd.read_csv(csv_file)

# Convert the 'Timestamp' column to datetime and extract day of the week and time intervals
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Extract day of the week and round timestamps to 15-minute intervals
df['DayOfWeek'] = df['Timestamp'].dt.day_name()
df['TimeOfDay'] = (df['Timestamp'].dt.floor('15min') + pd.Timedelta(hours=1)).dt.time  # Add 1-hour offset

# Filter data to be between 08:00 and 21:00
start_time = pd.to_datetime("09:00").time()
end_time = pd.to_datetime("22:00").time()
df = df[(df['TimeOfDay'] >= start_time) & (df['TimeOfDay'] <= end_time)]

# Group by DayOfWeek and TimeOfDay and calculate the mean Capacity
days_grouped = df.groupby(['DayOfWeek', 'TimeOfDay'])['Capacity'].mean().reset_index()

# Dictionary mapping weather descriptions to categories
weather_category_mapping = {
    "Clear sky": "Sunny",
    "Mainly clear": "Sunny",
    "Partly cloudy": "Cloudy",
    "Overcast": "Cloudy",
    "Fog": "Cloudy",
    "Depositing rime fog": "Cloudy",
    "Light drizzle": "Rainy",
    "Moderate drizzle": "Rainy",
    "Dense drizzle": "Rainy",
    "Light freezing drizzle": "Rainy",
    "Dense freezing drizzle": "Rainy",
    "Slight rain": "Rainy",
    "Moderate rain": "Rainy",
    "Heavy rain": "Rainy",
    "Light freezing rain": "Rainy",
    "Heavy freezing rain": "Rainy",
    "Slight snowfall": "Snowing",
    "Moderate snowfall": "Snowing",
    "Heavy snowfall": "Snowing",
    "Snow grains": "Snowing",
    "Slight rain showers": "Rainy",
    "Moderate rain showers": "Rainy",
    "Violent rain showers": "Rainy",
    "Slight snow showers": "Snowing",
    "Heavy snow showers": "Snowing",
    "Slight or moderate thunderstorm": "Stormy",
    "Thunderstorm with slight hail": "Stormy",
    "Thunderstorm with heavy hail": "Stormy"
}

df['WeatherCategory'] = df['CurrentWeatherType'].map(weather_category_mapping).fillna('Other')

weather_grouped = df.groupby(['WeatherCategory','TimeOfDay'])['Capacity'].mean().reset_index()



# Convert to JSON
weather_json_data = weather_grouped.to_json(orient="records")  # Convert DataFrame to JSON
days_json_data = days_grouped.to_json(orient="records")

response = {
    "weather": weather_json_data,
    "days": days_json_data
}
print(response)
