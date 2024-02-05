import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class VisualizeSpeeds():
    def __init__(self):
        self.csv_file='speed_test_log.csv'
    def read_speed_test_data(self):
        """
        Read speed test data from a CSV file and preprocess it.

        Args:
        - csv_file (str): Path to the CSV file containing speed test data.

        Returns:
        - pd.DataFrame: Preprocessed speed test data.
        """
        df = pd.read_csv(self.csv_file, parse_dates=['Timestamp'])
        df['Download_Speed_Mbps'] = pd.to_numeric(df['Download_Speed_Mbps'], errors='coerce')
        df['Upload_Speed_Mbps'] = pd.to_numeric(df['Upload_Speed_Mbps'], errors='coerce')
        df['connection_succed'] = df['connection_succed'].fillna(False)
        return df

    def split_data_into_segments(self, df):
        """
        Split speed test data into segments based on continuity of time.

        Args:
        - df (pd.DataFrame): Preprocessed speed test data.

        Returns:
        - list: List of segments, where each segment is a list of rows from the DataFrame.
        """
        segments = []
        current_segment = []
        for index, row in df.iterrows():
            if len(current_segment) == 0 or (row['Timestamp'] - current_segment[-1]['Timestamp']).seconds <= 1800:
                current_segment.append(row)
            else:
                segments.append(current_segment)
                current_segment = [row]
        if current_segment:
            segments.append(current_segment)
        return segments

    def plot_speed_test_results(self, df, segments):
        """
        Plot speed test results using area plot. An area is made from a continous collection of data. 
        A continous collection of data is defined as data collected without a disruption of more than 15 min.
        
        Args:
        - df (pd.DataFrame): Preprocessed speed test data.
        - segments (list): List of segments, where each segment is a list of rows from the DataFrame.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        for segment in segments:
            ax.fill_between([row['Timestamp'] for row in segment], [row['Download_Speed_Mbps'] for row in segment], color='blue', alpha=0.4)
        lost_connection_times = df[df['connection_succed'] == False]['Timestamp']
        for time_lost in lost_connection_times:
            ax.axvline(x=time_lost, color='r', linestyle='--', linewidth=0.7)
        ax.set_title('Download Speed over Time with Connection Loss')
        ax.set_xlabel('Time')
        ax.set_ylabel('Download Speed (Mbps)')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=8))
        fig.autofmt_xdate()
        plt.grid(True)
        ax.legend()
        plt.tight_layout()
        plt.show()

    def plot_speed_test(self):
        """
        Plot speed test results from a CSV file.

        Args:
        - csv_file (str): Path to the CSV file containing speed test data.
        """
        df = self.read_speed_test_data()
        segments = self.split_data_into_segments(df)
        self.plot_speed_test_results(df, segments)


if __name__ == "__main__":
    speed_visualizer = VisualizeSpeeds()
    speed_visualizer.plot_speed_test()
