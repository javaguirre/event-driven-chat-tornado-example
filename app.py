import tornado
import tornado.httpserver
from tornado.ioloop import IOLoop

from apps.chat.router import ChatRouter


class Application():
    def __init__(self, router):
        self.router = router
        self.application = tornado.web.Application(
            self.router.urls,
            debug=True,
            autoreload=True
        )

    def start(self):
        http_server = tornado.httpserver.HTTPServer(self.application)
        http_server.listen(8888)
        IOLoop.current().start()

application = Application(ChatRouter())
application.start()
