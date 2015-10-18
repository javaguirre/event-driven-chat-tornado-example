import redis

from .base_backend import BaseBackend, BaseMobileBackend


class RedisBackend(BaseBackend):
    '''
        We might want to delete, update
        or find one element, in this example
        is not necessary but in that case those
        methods should go to BaseBackend as abstract
        and be implemented here after
    '''

    def __init__(self, db=0):
        self.redis = redis.Redis(decode_responses=True, db=db)

    def find_all(self, **kwargs):
        return self.redis.lrange(
            kwargs['key'],
            kwargs['start'],
            kwargs['end']
        )


class RedisMobileBackend(BaseMobileBackend):
    '''
        Mobile device operations

        TODO regarding this class we could made the user_id
        an attribute of the class so we don't have to pass It
        all the time and also because the calls almost always depend on an
        user_id
    '''

    ANDROID = 'android'
    IOS = 'ios'
    DEVICES = (IOS, ANDROID)

    ANDROID_REDIS_KEY = 'reg_ids'
    IOS_REDIS_KEY = 'ios_ids'
    DEVICE_KEYS = {ANDROID: ANDROID_REDIS_KEY, IOS: IOS_REDIS_KEY}

    def __init__(self, db=0):
        self.redis = redis.Redis(decode_responses=True, db=db)
        self.device_type = None

    def get_user_key(self, user_id):
        return ':'.join(
            ['user', str(user_id), self.DEVICE_KEYS[self.device_type]]
        )

    def set_device(self, device_type):
        if self.device_valid(device_type):
            self.device_type = device_type

    def device_valid(self, device_type):
        if not device_type in self.DEVICES:
            raise AttributeError('Device not valid')

        return True

    def get_user_devices(self, user_id):
        return self.redis.smembers(self.get_user_key(user_id))

    def delete_device_id(self, user_id, device_id):
        self.redis.srem(self.get_key(user_id), device_id)

    def replace_device_id(self, user_id, device_id, new_device_id):
        key = self.get_key(user_id)

        self.redis.srem(key, device_id)
        self.redis.sadd(key, new_device_id)

    def add_device_id(self, user_id, device_id):
        self.redis.sadd(
            self.get_key(user_id),
            device_id
        )
