import logging

import numpy as np


class AutoReverse(object):
    def __init__(self):
        self.last_20_images = [np.zeros((120, 160, 3)) for _ in range(20)]
        self.counter = 0
        self.stopped_counter = 0
        self.reversing = False
        self.reverse_counter = 0
        self.constant_throttle = False

    def run(self, mode, constant_throttle, image):
        if mode != 'local_angle' or image is None or not constant_throttle:
            return False

        self.counter += 1

        if self.reversing:
            self.reverse_counter += 1
            if self.reverse_counter == 20:
                self.reversing = False
                self.reverse_counter = 0
                return True
            else:
                return False

        self.last_20_images.append(image)
        self.last_20_images.pop(0)

        if self.counter % 5 != 0:
            return False

        first_10_avg = np.array(self.last_20_images[:10]).mean()
        last_10_avg = np.array(self.last_20_images[10:]).mean()

        delta = abs(last_10_avg - first_10_avg)
        v = dict(
            mode=mode,
            first_10_avg=first_10_avg,
            last_10_avg=last_10_avg,
            diff=delta
        )

        logging.info(f"AutoReverse {v}")

        if delta < 0.3:
            if self.stopped_counter == 4:
                self.reversing = True
                self.reverse_counter = 1
                return True
            else:
                self.stopped_counter += 1

        return False

    def shutdown(self):
        pass
