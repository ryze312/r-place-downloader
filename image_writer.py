import io
from datetime import datetime
from time import sleep
import requests as req
from os.path import join as join_path
from PIL import Image
from io import BytesIO

class ImageWriter:

    def __init__(self, canvas_puller, image_dir, time_interval):
        self.canvas_puller = canvas_puller
        self.image_dir = image_dir
        self.time_interval = time_interval

    def get_image_path(self, timestamp):
        file_name = datetime.utcfromtimestamp(timestamp).strftime('%d_%m_%Y_%H_%M_%S') + ".png"
        return join_path(self.image_dir, file_name)

    def get_image(self, url):
        return req.get(url).content

    def merge_and_save(self, images, path):
        final_image = Image.new("RGBA", (2000, 2000))

        image_0 = Image.open(io.BytesIO(images[0]))
        image_1 = Image.open(io.BytesIO(images[1]))
        image_2 = Image.open(io.BytesIO(images[2]))
        image_3 = Image.open(io.BytesIO(images[3]))

        final_image.paste(image_0, (0, 0))
        final_image.paste(image_1, (1000, 0))
        final_image.paste(image_2, (0, 1000))
        final_image.paste(image_3, (1000, 1000))
        final_image.save(path, "PNG")

        image_0.close()
        image_1.close()
        image_2.close()
        image_3.close()
        final_image.close()

    def download_next_image(self):
        timestamp, urls = self.canvas_puller.pull_image_data()
        image_path = self.get_image_path(timestamp)

        images_data = []
        for url in urls:
            images_data.append(self.get_image(url))

        self.merge_and_save(images_data, image_path)

        return timestamp, urls, image_path

    def start(self):
        self.canvas_puller.renew_token()
        while True:
            yield self.download_next_image()
            sleep(self.time_interval)