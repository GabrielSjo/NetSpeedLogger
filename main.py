import csv
import speedtest
import time

def run_speed_test():
    try:
        # Initialize Speedtest
        st = speedtest.Speedtest()
        
        # Perform speed test
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

def log_speed_to_csv(timestamp, download_speed, upload_speed, success):
    with open('speed_test_log.csv', 'a', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Download_Speed_Mbps', 'Upload_Speed_Mbps', 'Success']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header if file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        
        # Write speed test results and success status
        writer.writerow({'Timestamp': timestamp,
                         'Download_Speed_Mbps': download_speed if success else None,
                         'Upload_Speed_Mbps': upload_speed if success else None,
                         'Success': success})
        if success:
            print("Speed test completed and logged.")
        else:
            print("Speed test failed. Retrying in 5 minutes...")

def main():
    while True:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        download_speed, upload_speed, success = run_speed_test()
        log_speed_to_csv(timestamp, download_speed, upload_speed, success)
        time.sleep(300)  # Wait for 5 minutes (300 seconds)

if __name__ == "__main__":
    main()
