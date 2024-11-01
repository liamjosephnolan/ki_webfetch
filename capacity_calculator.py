import pandas as pd

def calculate_average_capacity_by_interval(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Convert 'Timestamp' column to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Extract only the time component and round down to the nearest 15-minute interval
    df['TimeOfDay'] = df['Timestamp'].dt.floor('15T').dt.time

    # Filter times to include only those between 08:00 and 21:00
    start_time = pd.to_datetime("08:00").time()
    end_time = pd.to_datetime("21:00").time()
    df = df[(df['TimeOfDay'] >= start_time) & (df['TimeOfDay'] <= end_time)]

    # Group by 15-minute interval and calculate the average capacity
    average_capacity = df.groupby('TimeOfDay')['Capacity'].mean().reset_index()

    return average_capacity

if __name__ == "__main__":
    # Path to your CSV file
    csv_file = 'ki_current_capacity_log.csv'
    averages = calculate_average_capacity_by_interval(csv_file)
    print(averages)

