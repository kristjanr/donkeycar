import logging


class ThrottleFilter(object):
    '''
    allow reverse to trigger automatic reverse throttle
    '''

    def __init__(self):
        self.reverse_triggered = False
        self.last_throttle = 0.0

    def run(self, throttle_in):
        if throttle_in is None:
            return throttle_in

        throttle_out = throttle_in

        vs = dict(
            throttle_in=throttle_in,
            reverse_triggered=self.reverse_triggered,
            last_throttle=self.last_throttle
        )
        logging.info(f"ThrottleFilter Start {vs}")

        if throttle_out < 0.0: # hetkel tagurdab
            if not self.reverse_triggered and self.last_throttle < 0.0: # ei ole hetkel triggerdatud ja eelnevalt tagurdas
                throttle_out = 0.0 # jää seisma
                self.reverse_triggered = True # triggerda tagurdamine
        else:
            self.reverse_triggered = False

        self.last_throttle = throttle_out

        ve = dict(
            throttle_out=throttle_out,
            reverse_triggered=self.reverse_triggered,
            last_throttle=self.last_throttle
        )
        logging.info(f"ThrottleFilter End {ve}")

        return throttle_out

    def shutdown(self):
        pass
