import puller
import image_writer
import data
from datetime import datetime

ENDPOINT = "wss://gql-realtime-2.reddit.com/query"
REDDIT_USERNAME = None
REDDIT_PASSWORD = None
IMAGE_PATH = None
IMAGE_COUNT = 4  # There were 4 images at the end of r/place 2022
RENEWAL_RATE = None
PERIOD = None


def is_configured():
    return ENDPOINT and REDDIT_USERNAME and REDDIT_PASSWORD and IMAGE_PATH and IMAGE_COUNT and RENEWAL_RATE and PERIOD


def get_time_str(timestamp: int):
    return datetime.utcfromtimestamp(timestamp).strftime("%d-%m-%Y-%H-%M-%S")


if is_configured():
    connection_data = data.ConnectionData(REDDIT_USERNAME, REDDIT_PASSWORD, ENDPOINT)
    puller = puller.CanvasPuller(connection_data, RENEWAL_RATE, IMAGE_COUNT)
    image_writer = image_writer.ImageWriter(puller, IMAGE_PATH, PERIOD)

    for i, image_data in enumerate(image_writer.start()):
        print(f"Downloaded image {i + 1}")
        print(f"Time: {get_time_str(image_data[0])}")
        print(f"URLs: {image_data[1]}")
        print()
else:
    print("Configure script in main.py!")
