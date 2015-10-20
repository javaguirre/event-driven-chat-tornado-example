from collections import defaultdict

from tornado.websocket import WebSocketClosedError
import smokesignal

from events import Event


class WebSocketConnection(object):
    USER_WEBSOCKET_LIMIT = 3

    def __init__(self):
        self.clients = defaultdict(list)

    def limit_sockets_reached(self, user_id):
        return self.get_count(user_id) >= self.USER_WEBSOCKET_LIMIT

    def send(self, user_id, message):
        sent = False

        if not self.has(user_id):
            return sent

        sockets = self.get(user_id)

        for socket in sockets:
            sent = self.send_through_socket(socket, user_id, message) or sent

        return sent

    def send_through_socket(self, socket, user_id, message):
        sent = False

        try:
            socket.write_message(message)
            sent = True
        except WebSocketClosedError:
            self.close(user_id, socket)

        return sent

    def close(self, user_id, websocket):
        if self.has(user_id):
            smokesignal.emit(Event.USER_GONE, user_id)
            self.clients[user_id].remove(websocket)

    def get(self, user_id):
        return self.clients.get(user_id, [])

    def has(self, user_id):
        return user_id in self.clients

    def get_count(self, user_id):
        return len(self.get(user_id))

    def get_total_count(self):
        return len(self.clients)

    def add(self, user_id, websocket):
        self.clients[user_id].append(websocket)
