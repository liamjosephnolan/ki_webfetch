from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/average_capacity', methods=['GET'])
def average_capacity():
    # Path to your CSV file
    csv_file = 'ki_current_capacity_log.csv'
    
    def calculate_average_capacity_by_day_and_interval(csv_file):
        df = pd.read_csv(csv_file)
        
        # Convert the 'Timestamp' column to datetime and extract day of the week and time intervals
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['DayOfWeek'] = df['Timestamp'].dt.day_name()
        df['TimeOfDay'] = df['Timestamp'].dt.floor('15T').dt.time

        # Filter data to be between 08:00 and 21:00
        start_time = pd.to_datetime("08:00").time()
        end_time = pd.to_datetime("21:00").time()
        df = df[(df['TimeOfDay'] >= start_time) & (df['TimeOfDay'] <= end_time)]

        # Group by DayOfWeek and TimeOfDay and calculate the mean Capacity
        grouped = df.groupby(['DayOfWeek', 'TimeOfDay'])['Capacity'].mean().reset_index()
        
        # Convert the DataFrame to a nested dictionary format
        result = []
        for day in grouped['DayOfWeek'].unique():
            day_data = grouped[grouped['DayOfWeek'] == day]
            day_entry = {
                "DayOfWeek": day,
                "Data": [
                    {
                        "TimeOfDay": time.strftime('%H:%M'),  # Format time as HH:MM
                        "Capacity": round(capacity, 2)  # Optional: round to 2 decimal places
                    }
                    for time, capacity in zip(day_data['TimeOfDay'], day_data['Capacity'])
                ]
            }
            result.append(day_entry)
        
        return result
    
    # Generate the JSON structure and send it as a response
    averages = calculate_average_capacity_by_day_and_interval(csv_file)
    return jsonify(averages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

