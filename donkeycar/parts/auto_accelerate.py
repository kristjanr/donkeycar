import logging

import numpy as np


class AutoAccelerate(object):
    def __init__(self):
        self.last_20_images = [np.zeros((120, 160, 3)) for _ in range(20)]
        self.counter = 0
        self.constant_throttle = False

    def run(self, mode, constant_throttle, image):
        if mode != 'local_angle' or image is None or not constant_throttle:
            return 0

        self.counter += 1
        self.last_20_images.append(image)
        self.last_20_images.pop(0)

        if self.counter % 5 != 0:
            return 0

        first_10_avg = np.array(self.last_20_images[:10]).mean()
        last_10_avg = np.array(self.last_20_images[10:]).mean()

        delta = abs(last_10_avg - first_10_avg)
        v = dict(
            mode=mode,
            first_10_avg=first_10_avg,
            last_10_avg=last_10_avg,
            diff=delta
        )

        logging.info(f"AutoAccelerate {v}")

        if delta < 0.3:
            return 1

        return 0

    def shutdown(self):
        pass
