from abc import ABC, abstractmethod

class IStorageBackend(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass