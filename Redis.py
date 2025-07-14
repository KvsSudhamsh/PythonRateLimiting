from istorage import IStorageBackend
from redis import Redis

class RedisStorage(IStorageBackend):
    def __init__(self, host = '10.0.0.20', port = 6379, db = 0):
        self.client = Redis(host = '10.0.0.20', port = port, db = db)
    
    def get(self, key):
        return self.client.get(key)

    def set(self, key, value):
        self.client.set(key, value)
    