import asyncio
import websockets as ws
import json
import requests as req
from lxml import html
from time import sleep


class CanvasPuller:
    def __init__(self, connection_data, renewal_rate, canvas_parts):
        self.socket = None
        self.connection_data = connection_data
        self.renewal_rate = renewal_rate
        self.canvas_parts = canvas_parts
        self.image_count = 0

    def pull_image_data(self):
        if self.image_count % self.rene == 0:
            self.renew_token()

        self.image_count += 1
        return asyncio.run(self.connect_and_pull())

    def renew_token(self):
        print("Renewing token!")

        with req.Session() as session:
            resp = session.get(self.connection_data.reddit_login_url)
            login_page = html.fromstring(resp.text)
            csrf_token = login_page.xpath("//input[@name='csrf_token']")[0].value

            auth_data = {
                "username": self.connection_data.username,
                "password": self.connection_data.password,
                "dest": self.connection_data.reddit_login_url,
                "csrf_token": csrf_token
            }

            resp = session.post(self.connection_data.reddit_login_url, data=auth_data)
            sleep(1.5)

            assert resp.status_code == 200  # I am too lazy to properly exit and print error lol

            resp = session.get(self.connection_data.reddit_url)
            main_page = html.fromstring(resp.text)
            json_str = main_page.xpath("//script[@id='data']")[0].text[len("window.__r = "):-1]
            json_data = json.loads(json_str)
            self.connection_data.token = json_data["user"]["session"]["accessToken"]
            self.connection_data.update_ws_auth()

    async def connect(self):
        await self.socket.send(json.dumps(self.connection_data.ws_auth))
        await self.socket.send(json.dumps(self.connection_data.config))
        await self.socket.send(json.dumps(self.connection_data.config_2))
        response = json.loads(await self.socket.recv())
        return response

    async def is_auth(self, response):
        return response["payload"]["message"] != "401: 401 Unauthorized"

    async def try_connecting(self):
        try:
            response = await self.connect()
            if response["type"] != "connection_ack":
                if not await self.is_auth(response):
                    await self.socket.close()
                    self.renew_token()
                    self.socket = await ws.connect(self.connection_data.endpoint, extra_headers=self.connection_data.headers)
                    response = await self.connect()

                    if not await self.is_auth(response):
                        print(response)
                        print("401! Invalid credentials or something is wrong")
                        return False

                else:
                    print("Wrong response type! Should be connection_ack")
                    print("Details below: ")
                    print(response)
                return False

        except ws.ConnectionClosedError as e:
            print("Connection aborted")
            print("Details below: ")
            print(e)
            return False
        return True

    @staticmethod
    async def is_full_frame_message(data):
        try:
            return data["payload"]["data"]["subscribe"]["data"]["__typename"] == "FullFrameMessageData"
        except KeyError:
            return False

    @staticmethod
    async def parse_full_frame(data):
        subscribe_data = data["payload"]["data"]["subscribe"]["data"]
        return subscribe_data["timestamp"], subscribe_data["name"]

    async def request_new_canvas(self, index):
        await self.socket.send(json.dumps(self.connection_data.canvas_confs[index]))

    async def get_frames(self):
        frame_datas = []
        index = 0
        async for message in self.socket:
            data = json.loads(message)
            if await self.is_full_frame_message(data):
                frame_datas.append(await self.parse_full_frame(data))

                if len(frame_datas) == self.canvas_parts:
                    return frame_datas

                await self.request_new_canvas(index)
                index += 1

    async def parse_frames(self, frames):
        timestamp = frames[1][0]
        timestamp //= 1000
        return timestamp, (frames[0][1], frames[1][1], frames[2][1], frames[3][1])

    async def connect_and_pull(self):
        self.socket = await ws.connect(self.connection_data.endpoint, extra_headers=self.connection_data.headers)

        is_connected = await self.try_connecting()
        if is_connected:
            frames = await self.parse_frames(await self.get_frames())
            await self.socket.close()
            return frames
