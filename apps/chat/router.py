import tornado

from .handlers import (
    WebSocketHandler, MessageHandler, WebHandler
)

from .connection import WebSocketConnection


class ChatRouter(object):
    urls = [
        (r'/messages/', MessageHandler),
        (
            r'/websocket/(.*)',
            WebSocketHandler,
            {'connection': WebSocketConnection()}
        ),
        (
            r'/static/(.*)',
            tornado.web.StaticFileHandler,
            {'path': 'apps/chat/static'}
        ),
        (r'/', WebHandler)
    ]
