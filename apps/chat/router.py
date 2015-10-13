from .handlers import (
    WebSocketHandler, MessageHandler, WebHandler
)


class ChatRouter(object):
    urls = [
        (r'/messages/', MessageHandler),
        (r'/websocket/(.*)', WebSocketHandler),
        (r'/', WebHandler)
    ]
