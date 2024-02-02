import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_speed_test_results(csv_file):
    # Read CSV into a DataFrame
    df = pd.read_csv(csv_file, parse_dates=['Timestamp'])

    # Handle missing values
    df['Download_Speed_Mbps'] = pd.to_numeric(df['Download_Speed_Mbps'], errors='coerce')
    df['Upload_Speed_Mbps'] = pd.to_numeric(df['Upload_Speed_Mbps'], errors='coerce')
    df['connection_succed'] = df['connection_succed'].fillna(False)

    # Plot download speeds over time
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['Timestamp'], df['Download_Speed_Mbps'], marker='o', linestyle='-', label='Download Speed')

    # Mark times when connection is lost as vertical lines
    lost_connection_times = df[df['connection_succed'] == False]['Timestamp']
    for time_lost in lost_connection_times:
        ax.axvline(x=time_lost, color='r', linestyle='--')

    # Formatting the plot
    ax.set_title('Download Speed over Time with Connection Loss')
    ax.set_xlabel('Time')
    ax.set_ylabel('Download Speed (Mbps)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    fig.autofmt_xdate()  # Rotate x-axis labels for better readability
    plt.grid(True)
    plt.tight_layout()

    # Add legend
    ax.legend()

    # Show plot
    plt.show()

if __name__ == "__main__":
    plot_speed_test_results('speed_test_log.csv')
