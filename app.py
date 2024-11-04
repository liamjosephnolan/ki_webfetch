from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/average_capacity', methods=['GET'])
def average_capacity():
    # Path to your CSV file
    csv_file = 'ki_current_capacity_log.csv'
    
    def calculate_average_capacity_by_day_of_week(csv_file):
        df = pd.read_csv(csv_file)
        # Parse 'Timestamp' column as datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        # Extract the day of the week and assign it as a new column
        df['DayOfWeek'] = df['Timestamp'].dt.day_name()
        
        # Group by 'DayOfWeek' and calculate the average 'Capacity'
        average_capacity = df.groupby('DayOfWeek')['Capacity'].mean().reset_index()
        
        # Sort days of the week for logical ordering
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        average_capacity['DayOfWeek'] = pd.Categorical(average_capacity['DayOfWeek'], categories=day_order, ordered=True)
        average_capacity = average_capacity.sort_values('DayOfWeek')
        
        # Convert to list of dictionaries for JSON response
        return average_capacity.to_dict(orient='records')
    
    averages = calculate_average_capacity_by_day_of_week(csv_file)
    return jsonify(averages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

