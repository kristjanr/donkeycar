import logging

import numpy as np


class AutoAccelerate(object):
    def __init__(self):
        self.last_20_images = [np.zeros((120, 160, 3)) for _ in range(20)]
        self.counter = 0
        self.constant_throttle = False
        self.accelerated = True
        self.extra_throttle = 0.1

    logging.info(f"AutoAccelerate started!")

    def run(self, mode, constant_throttle, image):
        extra_throttle = 0
        if mode != 'local_angle' or image is None or not constant_throttle:
            return extra_throttle

        self.counter += 1
        self.last_20_images.append(image)
        self.last_20_images.pop(0)

        if self.counter % 5 != 0:
            return extra_throttle

        first_10_avg = np.array(self.last_20_images[:10]).mean()
        last_10_avg = np.array(self.last_20_images[10:]).mean()

        delta = abs(last_10_avg - first_10_avg)
        if delta < 0.3:
            self.accelerated = True
            extra_throttle = self.extra_throttle
        elif self.accelerated:
            self.accelerated = False
            extra_throttle = -self.extra_throttle

        v = dict(
            diff=delta,
            extra_throttle=extra_throttle
        )
        logging.info(f"AutoAccelerate {v}")
        return extra_throttle

    def shutdown(self):
        pass
