import logging

import numpy as np


class AutoReverse(object):
    accepted_modes = {'local_angle', 'reversing'}

    def __init__(self):
        self.last_20_images = [np.zeros((120, 160, 3)) for _ in range(20)]
        self.counter = 0
        self.stopped_counter = 0
        self.reverse_counter = 0
        self.constant_throttle = False
        logging.info(f"AutoReverse started!")

    def run(self, mode, constant_throttle, image):
        if mode not in self.accepted_modes or image is None or not constant_throttle:
            self.stopped_counter = 0
            self.reverse_counter = 0
            return mode

        self.counter += 1

        if mode == 'reversing':
            self.reverse_counter += 1
            v = dict(
                stopped_counter=self.stopped_counter,
                reverse_counter=self.reverse_counter,
                mode=mode,
            )
            logging.info(f"AutoReverse {v}")
            if self.reverse_counter == 40:
                self.reverse_counter = 0
                return 'local_angle'
            else:
                return 'reversing'

        self.last_20_images.append(image)
        self.last_20_images.pop(0)

        if self.counter % 5 != 0:
            return False

        first_10_avg = np.array(self.last_20_images[:10]).mean()
        last_10_avg = np.array(self.last_20_images[10:]).mean()

        delta = abs(last_10_avg - first_10_avg)
        v = dict(
            stopped_counter=self.stopped_counter,
            reverse_counter=self.reverse_counter,
            mode=mode,
            diff=delta
        )
        logging.info(f"AutoReverse {v}")

        if delta < 0.3:
            if self.stopped_counter == 3:
                self.stopped_counter = 0
                return 'reversing'
            else:
                self.stopped_counter += 1

        return mode

    def shutdown(self):
        pass
