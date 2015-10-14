import logging

from blinker import signal

from events import Event
from lib.notifications import AndroidNotification, IosNotification


class AndroidListener():
    def __init__(self, options):
        self.gcm_key = options.gcm

        signal(Event.NEW_MESSAGE).connect(self.send)

    def send(self, message):
        logging.info('SENT ON ANDROID')
        logging.info(message)

        notification = AndroidNotification(self.gcm_key)
        notification.set_receptor(message['user_id'])

        notification.send(message)


class IosListener():
    def __init__(self, options):
        self.cert = options.cert
        self.key = options.key
        self.sandbox = options.sandbox

        signal(Event.NEW_MESSAGE).connect(self.send)

    def send(self, message):
        logging.info('SENT ON IOS')
        logging.info(message)

        notification = IosNotification(
            self.cert,
            self.key,
            self.sandbox
        )
        notification.set_badge(message.pop('ios_badge'))
        notification.set_receptor(message['user_id'])
        notification.set_loc_key(message.pop('loc_key'))
        notification.set_loc_args(message.pop('loc_args'))

        notification.send(message)


class PersistListener():
    def __init__(self, options):
        signal(Event.NEW_MESSAGE).connect(self.persist)
        signal(Event.NEW_DEVICE).connect(self.persist_device)

    def persist(self, message):
        # self.backend.save(message)
        pass

    def persist_device(self, device_id):
        # self.mobile_backend.save_device(device_id)
        pass
