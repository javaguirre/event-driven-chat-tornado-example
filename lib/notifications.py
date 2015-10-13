import logging
from abc import abstractmethod
import time
import random

from gcm import GCM
from apns import APNs, Payload, Frame, PayloadAlert

from backend import MobileBackend


class Notification(object):
    def set_receptor(self, receptor):
        self.receptor = receptor

    def get_devices(self):
        return list(self.backend.get_user_device_ids(self.receptor))

    @abstractmethod
    def send(self, message):
        pass


class AndroidNotification(Notification):
    CANONICAL = 'canonical_id'
    ERROR = 'errors'
    ERROR_EXCEPTIONS = ('NotRegistered', 'InvalidRegistration')

    def __init__(self, gcm_key):
        self.gcm = GCM(gcm_key)
        self.backend = MobileBackend(MobileBackend.ANDROID)

    def send(self, message):
        device_ids = self.get_devices()

        if len(device_ids) == 0:
            return False

        response = self.gcm.json_request(
            registration_ids=device_ids,
            data=message
        )

        return self.process_response(response)

    def process_response(self, response):
        success = False

        if self.ERROR in response:
            self.delete_old_devices(response)
        else:
            success = True

        if self.CANONICAL in response:
            self.update_canonical_ids(response)

        return success

    def delete_old_devices(self, response):
        for error, device_ids in response[self.ERROR].items():
            if error in self.ERROR_EXCEPTIONS:
                for device_id in device_ids:
                    self.backend.delete_device_id(self.receptor, device_id)

    def update_canonical_ids(self, response):
        for device_id, canonical_id in response[self.CANONICAL].items():
            self.backend.replace_device_id(
                self.receptor, device_id, canonical_id
            )


class IosNotification(Notification):
    IOS_EXPIRY_SECONDS = time.time() + 3600
    IOS_PRIORITY = 10
    DEFAULT_SOUND = 'default'
    LOC_KEY_ERROR_MESSAGE = 'IosNotification should have loc_key defined'

    def __init__(self, cert, key, sandbox):
        self.apns = APNs(
            use_sandbox=sandbox,
            cert_file=cert,
            key_file=key,
            enhanced=True
        )
        self.backend = MobileBackend(MobileBackend.IOS)

        self.error_callback = self.response_listener
        self.loc_args = []
        self.badge = None
        self.loc_key = None

    def response_listener(error_response):
        logging.error(': '.join(['IOS ERROR', str(error_response)]))

    def send(self, message):
        success = False

        if not self.loc_key:
            raise AttributeError(self.LOC_KEY_ERROR_MESSAGE)

        device_tokens = self.get_devices()

        if len(device_tokens):
            success = True

        frame = self.get_frame(message, device_tokens)

        self.apns.gateway_server.send_notification_multiple(frame)
        self.apns.gateway_server.register_response_listener(
            self.error_callback
        )

        return success

    def get_frame(self, message, device_tokens):
        frame = Frame()
        identifier = random.getrandbits(32)
        payload_alert = PayloadAlert(
            loc_key=self.loc_key,
            loc_args=self.loc_args
        )
        payload = Payload(
            alert=payload_alert,
            custom=message,
            sound=self.DEFAULT_SOUND,
            badge=self.badge
        )

        for token in device_tokens:
            frame.add_item(
                token,
                payload,
                identifier,
                self.IOS_EXPIRY_SECONDS,
                self.IOS_PRIORITY
            )

        return frame
