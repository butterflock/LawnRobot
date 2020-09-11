import datetime
from abc import abstractmethod, ABC


class Camera(ABC):

    @abstractmethod
    def get_frame(self):
        pass

    def release(self):
        pass

    def get_timestamp(self):
        return datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")
