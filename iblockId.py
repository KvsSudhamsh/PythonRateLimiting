from abc import ABC, abstractmethod

class IBlockId(ABC):
    @abstractmethod
    def blockId(self):
        pass