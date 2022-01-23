import logging


class AutoAccelerate(object):
    def __init__(self):
        pass

    def run(self, throttle_in, mode, image):

        v = dict(
            throttle_in=throttle_in,
            mode=mode,
            image_shp=image.shape
        )
        logging.info(f"AutoAccelerate {v}")

        return throttle_in

    def shutdown(self):
        pass
