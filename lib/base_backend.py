from abc import ABCMeta, abstractmethod


class BaseMobileBackend(object):
    '''
        Abstract mobile backend for
        device persist operations
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_device(self, device_type):
        pass

    @abstractmethod
    def get_user_devices(self, user_id):
        pass

    @abstractmethod
    def delete_device_id(self, user_id, device_id):
        pass

    @abstractmethod
    def replace_device_id(self, user_id, device_id):
        pass

    @abstractmethod
    def add_device_id(self, user_id, device_id):
        pass


class BaseBackend():
    '''
        Abstract backend for
        chat operations
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def find_all(self, **kwargs):
        pass
