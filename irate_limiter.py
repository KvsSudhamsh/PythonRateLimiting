from abc import ABC,abstractmethod

class IRateLimiter(ABC):
    @abstractmethod
    def is_allowed(self, client_id:str):
        pass