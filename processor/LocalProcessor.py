import cv2

from processor.Processor import Processor
from run import PerceptionUpdate


class LocalProcessor(Processor):

    def process(self, update: PerceptionUpdate):
        cv2.imshow("frame", cv2.cvtColor(cv2.addWeighted(update.camera, 0.7, update.get_colored_seg(), 0.3, 0), cv2.COLOR_RGB2BGR))
        cv2.waitKey(1)

    def shutdown(self):
        cv2.destroyAllWindows()
