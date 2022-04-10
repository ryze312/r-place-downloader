class ConnectionData:
    def __init__(self, username, password, endpoint):
        self.token = None  #"392261997529-yrSYoQ92n-3en-EaVX4vb_XxAiY3SQ"
        self.username = username
        self.password = password
        self.endpoint = endpoint

        self.reddit_url = "https://reddit.com"
        self.reddit_login_url = "https://reddit.com/login"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 "
                          "Safari/537.36",
            "Origin": "https://hot-potato.reddit.com"
        }
        self.ws_auth = {
            "type": "connection_init",
            "payload": {
                "Authorization": f"Bearer {self.token}"
            }
        }
        self.config = {"id": "1", "type": "start",
                  "payload": {"variables": {"input": {"channel": {"teamOwner": "AFD2022", "category": "CONFIG"}}},
                              "extensions": {}, "operationName": "configuration",
                              "query": "subscription configuration($input: SubscribeInput!) {\n  subscribe(input: $input) {\n    id\n    ... on BasicMessage {\n      data {\n        __typename\n        ... on ConfigurationMessageData {\n          colorPalette {\n            colors {\n              hex\n              index\n              __typename\n            }\n            __typename\n          }\n          canvasConfigurations {\n            index\n            dx\n            dy\n            __typename\n          }\n          canvasWidth\n          canvasHeight\n          __typename\n        }\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}}
        self.config_2 = {"id": "2", "type": "start", "payload": {
            "variables": {"input": {"channel": {"teamOwner": "AFD2022", "category": "CANVAS", "tag": "0"}}},
            "extensions": {}, "operationName": "replace",
            "query": "subscription replace($input: SubscribeInput!) {\n  subscribe(input: $input) {\n    id\n    ... on BasicMessage {\n      data {\n        __typename\n        ... on FullFrameMessageData {\n          __typename\n          name\n          timestamp\n        }\n        ... on DiffFrameMessageData {\n          __typename\n          name\n          currentTimestamp\n          previousTimestamp\n        }\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}}

        second_canvas_conf = {
    "id": "3",
    "type": "start",
    "payload": {
        "variables": {
            "input": {
                "channel": {
                    "teamOwner": "AFD2022",
                    "category": "CANVAS",
                    "tag": "1"
                }
            }
        },
        "extensions": {},
        "operationName": "replace",
        "query": "subscription replace($input: SubscribeInput!) {\n  subscribe(input: $input) {\n    id\n    ... on BasicMessage {\n      data {\n        __typename\n        ... on FullFrameMessageData {\n          __typename\n          name\n          timestamp\n        }\n        ... on DiffFrameMessageData {\n          __typename\n          name\n          currentTimestamp\n          previousTimestamp\n        }\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }

}
        third_canvas_confg = {
    "id": "3",
    "type": "start",
    "payload": {
        "variables": {
            "input": {
                "channel": {
                    "teamOwner": "AFD2022",
                    "category": "CANVAS",
                    "tag": "2"
                }
            }
        },
        "extensions": {},
        "operationName": "replace",
        "query": "subscription replace($input: SubscribeInput!) {\n  subscribe(input: $input) {\n    id\n    ... on BasicMessage {\n      data {\n        __typename\n        ... on FullFrameMessageData {\n          __typename\n          name\n          timestamp\n        }\n        ... on DiffFrameMessageData {\n          __typename\n          name\n          currentTimestamp\n          previousTimestamp\n        }\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
}
        fourth_canvas_conf = {
    "id": "4",
    "type": "start",
    "payload": {
        "variables": {
            "input": {
                "channel": {
                    "teamOwner": "AFD2022",
                    "category": "CANVAS",
                    "tag": "3"
                }
            }
        },
        "extensions": {},
        "operationName": "replace",
        "query": "subscription replace($input: SubscribeInput!) {\n  subscribe(input: $input) {\n    id\n    ... on BasicMessage {\n      data {\n        __typename\n        ... on FullFrameMessageData {\n          __typename\n          name\n          timestamp\n        }\n        ... on DiffFrameMessageData {\n          __typename\n          name\n          currentTimestamp\n          previousTimestamp\n        }\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
}
        self.canvas_confs = [second_canvas_conf, third_canvas_confg, fourth_canvas_conf]

    def update_ws_auth(self):
        self.ws_auth = {
            "type": "connection_init",
            "payload": {
                "Authorization": f"Bearer {self.token}"
            }
        }