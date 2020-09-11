from abc import ABC, abstractmethod


class DriveController(ABC):
    @abstractmethod
    def turn_right(self):
        pass

    @abstractmethod
    def turn_left(self):
        pass

    @abstractmethod
    def straight(self, speed):
        pass

    @abstractmethod
    def backwards(self, speed):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    async def get_info(self):
        pass
