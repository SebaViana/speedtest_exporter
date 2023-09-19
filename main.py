import os
import time
import yaml
import speedtest
from prometheus_client import start_http_server, Gauge

download_speed_metric = Gauge('download_speed_mbps', 'Download speed in Mbps')
upload_speed_metric = Gauge('upload_speed_mbps', 'Upload speed in Mbps')

def get_speed():
    try:
        st = speedtest.Speedtest(secure=True)
        st.get_best_server()

        download_speed = st.download() / 1_000_000  
        upload_speed = st.upload() / 1_000_000  

        return download_speed, upload_speed
    except speedtest.SpeedtestBestServerFailure as e:
        print(f"Error getting server: {e}")
        return None, None
    except Exception as e:
        print(f"Error during speed test: {e}")
        return None, None

def read_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Config file '{config_file}' not found.")
        config = {}

    default_config_file = "default.yml"
    with open(default_config_file, 'r') as default_file:
        default_config = yaml.safe_load(default_file)

    config = {**default_config, **config}

    return config

def main():
    config_file = "custom.yml"

    config = read_config(config_file)

    http_port = int(os.environ.get('HTTP_PORT', 8085))

    start_http_server(http_port)

    speedtest_interval = config['speedtest_interval']

    while True:
        download_speed, upload_speed = get_speed()
        
        if download_speed is not None and upload_speed is not None:
            download_speed_metric.set(download_speed)
            upload_speed_metric.set(upload_speed)

        time.sleep(speedtest_interval)

if __name__ == "__main__":
    main()
