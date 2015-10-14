import tornado
import tornado.httpserver
from tornado.ioloop import IOLoop

from apps.chat.router import ChatRouter
from apps.chat.listeners import AndroidListener, IosListener, PersistListener
from lib.options import get_options


class Application():
    def __init__(self, router):
        self.options = get_options()
        self.router = router
        self.application = tornado.web.Application(
            self.router.urls,
            debug=True,
            autoreload=True
        )
        self.listeners = [AndroidListener, IosListener, PersistListener]
        self.started_listeners = []

    def start_listeners(self):
        for listener in self.listeners:
            self.started_listeners.append(listener(self.options))

    def start_server(self):
        http_server = tornado.httpserver.HTTPServer(self.application)
        http_server.listen(8888)
        IOLoop.current().start()

    def start(self):
        self.start_listeners()
        self.start_server()

application = Application(ChatRouter())
application.start()
