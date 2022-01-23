import logging


class AutoAccelerate(object):
    def __init__(self):
        pass

    def run(self, throttle_in, mode, image):
        img_shp = image.shape if image is not None else None
        v = dict(
            throttle_in=throttle_in,
            mode=mode,
            image_shp=img_shp
        )
        logging.info(f"AutoAccelerate {v}")

        return throttle_in

    def shutdown(self):
        pass
