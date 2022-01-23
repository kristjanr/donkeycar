import logging

import numpy as np


class AutoAccelerate(object):
    def __init__(self):
        self.last_20_images = [np.zeros((120, 160, 3)) for _ in range(20)]
        self.counter = 0

    def run(self, mode, image):
        if mode != 'local_angle' or image is None:
            return 0

        self.counter += 1
        self.last_20_images.append(image)
        self.last_20_images.pop(0)

        if self.counter % 20 != 0:
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

        if delta < 1:
            return 0.05

        return 0

    def shutdown(self):
        pass
