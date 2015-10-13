import logging
import json

import smokesignal
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler as TornadoWebSocketHandler

from events import Event


class WebSocketHandler(TornadoWebSocketHandler):
    def send_ping(self):
        '''
            Using ping you can check if the connection
            was closed and try to open again
        '''
        return self.ping('PING')

    def on_pong(self, data):
        pass

    def open(self, user_id):
        self.user_id = user_id
        self.connection.add(self.user_id, self)

        logging.info('NUMBER CLIENTS: %d' %
                     self.connection.count())

    def on_message(self, message):
        smokesignal.emit(Event.NEW_MESSAGE, message)

    def on_close(self):
        self.connection.close(self.user_id, self)

    def check_origin(self, origin):
        # TODO You need to authorize the websocket
        # check the origin of the connection, check if the user
        # is authorized
        return True


class MessageHandler(RequestHandler):
    def get(self, user_id):
        '''
          You could get the users messages
          here if in mobile devices not
          implementing Websockets
        '''
        pass

    def post(self, user_id):
        '''
            This method is for convenience, in case we don't
            want to implement websocket on mobile devices,
            we will use this connection to create messages
        '''
        message = self.request.body
        smokesignal.emit(Event.NEW_MESSAGE, message)

        self.write(json.dumps(message))


class WebHandler(RequestHandler):
    '''
        Websocket front example, this would be in
        our Web application and we would connect
        to It through a TCP socket
    '''

    def get(self, user_id=None):
        self.render('templates/web.html')
