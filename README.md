# NetSpeedLogger
This Python script is designed to collect, log, and visualize network speeds at regular intervals using the Speedtest.net service. It runs a speed test every 5 minutes, logs the results to a CSV file, and provides visualizations of the collected data using matplotlib.

# Requirements

The script requires Python 3.x and the following dependencies:

    speedtest-cli==2.1.3
    matplotlib==3.4.3

Install the dependencies using pip:

    pip install -r requirements.txt

# Usage

Run the script:

    python network_speed_logger.py