import random
import asyncio
import aiohttp


class Sensor:
    def __init__(self, sensor_config, logging_url):
        self.type = sensor_config["type"]
        self.valid_range = sensor_config["valid_range"]
        self.logging_url = logging_url

    async def read_data(self):
        while True:
            # calc an error in measurements of 5%
            error = self.valid_range[1] * 0.05
            # Simulate sensor data with error - creates some values out of range
            data = random.uniform(self.valid_range[0] - error, self.valid_range[1] + error)

            # Check if data is within the valid range
            if not self.is_data_valid(data):
                await self.log_invalid_data(data)

            await asyncio.sleep(SensorService.sleep_interval)

    def is_data_valid(self, data):
        return self.valid_range[0] <= data <= self.valid_range[1]

    async def log_invalid_data(self, data):
        # logging invalid values
        if data > self.valid_range[1]:
            log_message = f"invalid measurement of {self.type}: {round(data, 3)} (Exceeds max value)"
        else:
            log_message = f"invalid measurement of {self.type}: {round(data, 3)} (Fell below minimum value)"

        async with aiohttp.ClientSession() as session:
            async with session.post(self.logging_url, json={"message": log_message}) as res:
                if res.status == 200:
                    print(f"{self.type} Sensor - {log_message} - Logged successfully")
                else:
                    print(f"{self.type} Sensor - {log_message} - Failed to log data")


class SensorService:
    sleep_interval = 0.25  # Default sleep interval

    def __init__(self, sensors):
        self.sensors = sensors

    async def start_monitoring(self):
        tasks = [sensor.read_data() for sensor in self.sensors]
        await asyncio.gather(*tasks)
