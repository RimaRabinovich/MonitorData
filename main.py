import json

from sensor_service import *

if __name__ == "__main__":

    # read sensor configuration file
    with open("sensor_config.json", "r") as config_file:
        sensors_config = json.load(config_file)["sensors"]

    # url for logging service
    logging_url = "http://localhost:5000/log"

    # create instances of sensors
    sensors = [Sensor(config, logging_url) for config in sensors_config]

    # create an instance of the SensorService
    sensor_service = SensorService(sensors)

    # Start monitoring
    asyncio.run(sensor_service.start_monitoring())
