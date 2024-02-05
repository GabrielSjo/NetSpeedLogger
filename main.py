import csv
import speedtest
import time

class SpeedTestApp:
    def __init__(self):
        self.csv_file='speed_test_log.csv'

    def run_speed_test(self):
        """
        Perform a speed test and return the download and upload speeds.

        Returns:
        - float: Download speed in Mbps.
        - float: Upload speed in Mbps.
        - bool: True if the speed test is successful, False otherwise.
        """
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 1e+6  # Convert to Mbps
            upload_speed = st.upload() / 1e+6      # Convert to Mbps
            return download_speed, upload_speed, True
        except speedtest.ConfigRetrievalError as e:
            print(f"Speed test failed: {e}")
            return None, None, False
        except Exception as e:
            print(f"An error occurred during speed test: {e}")
            return None, None, False

    def log_speed_to_csv(self, timestamp, download_speed, upload_speed, success):
        """
        Log speed test results to a CSV file.

        Args:
        - timestamp (str): Timestamp of the speed test.
        - download_speed (float): Download speed in Mbps.
        - upload_speed (float): Upload speed in Mbps.
        - success (bool): True if the speed test is successful, False otherwise.
        """
        with open('speed_test_log.csv', 'a', newline='') as csvfile:
            fieldnames = ['Timestamp', 'Download_Speed_Mbps', 'Upload_Speed_Mbps', 'Success']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'Timestamp': timestamp,
                            'Download_Speed_Mbps': download_speed if success else None,
                            'Upload_Speed_Mbps': upload_speed if success else None,
                            'Success': success})
            if success:
                print("Speed test completed and logged.")
            else:
                print("Speed test failed. Retrying in 5 minutes...")

    def main(self):
        """
        Main function to run the speed test and log results to a CSV file.
        """
        while True:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            download_speed, upload_speed, success = self.run_speed_test()
            self.log_speed_to_csv(timestamp, download_speed, upload_speed, success)
            time.sleep(300)


if __name__ == "__main__":
    app = SpeedTestApp()
    app.main()
