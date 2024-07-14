import redis
import random
import math
import time
import datetime

MAX_STORE_DATA = 360


class DataGenerator:
    def __init__(self):
        self.redis_client = redis.Redis(
            host="localhost", port=6379, decode_responses=True
        )
        self.running = False

    def run(self):
        self.running = True

        while self.running:
            for i in range(360):
                data = 30 + (10 * math.sin(math.radians(i))) + random.uniform(0, 2)
                redis_data = self.redis_client.hgetall("temp")

                keys = sorted(redis_data.keys())
                if len(keys) > MAX_STORE_DATA:
                    remove_keys = keys[: len(keys) - MAX_STORE_DATA]
                    for key in remove_keys:
                        self.redis_client.hdel("temp", key)

                key = datetime.datetime.now().isoformat()
                self.redis_client.hset("temp", mapping={key: data})

                print("update", key, data)
                time.sleep(1)


if __name__ == "__main__":
    generator = DataGenerator()
    generator.run()
