from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/api/average_capacity', methods=['GET'])
def average_capacity():
    # Path to your CSV file
    csv_file = 'ki_current_capacity_log.csv'
    
    def calculate_average_capacity_by_interval(csv_file):
        df = pd.read_csv(csv_file)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['TimeOfDay'] = df['Timestamp'].dt.floor('15T').dt.time
        start_time = pd.to_datetime("08:00").time()
        end_time = pd.to_datetime("21:00").time()
        df = df[(df['TimeOfDay'] >= start_time) & (df['TimeOfDay'] <= end_time)]
        average_capacity = df.groupby('TimeOfDay')['Capacity'].mean().reset_index()
        average_capacity['TimeOfDay'] = average_capacity['TimeOfDay'].astype(str)
        return average_capacity.to_dict(orient='records')
    
    averages = calculate_average_capacity_by_interval(csv_file)
    return jsonify(averages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

