class TurnBoost():
    '''
    This part will apply a thrust during turns where angles are extreme enough to cause the slowdown of the car.
    This is to help in turning when the car slows down because of friction or voltage drop caused by servo usage.
    This has two goals:
    1. To maintain a constant actual speed of the car throughout the track
    2. Avoid it stopping completely during tight and long turns whend driving slowly.
    '''

    def __init__(self, config: dict):
        self.positive_angles = {k: v for k, v in config.items() if k > 0}
        self.negative_angles = {k: v for k, v in config.items() if k < 0}
        self.enabled = False

    def toggle(self):
        self.enabled = not self.enabled
        print(f'TurnBoost is {"enabled" if self.enabled else "disabled"}.')

    def run(self, mode, current_angle, current_throttle):
        if mode == "user" and self.enabled:
            for angle, boost in self.positive_angles.items():
                if current_angle >= angle:
                    new_throttle = current_throttle + boost
                    print(f'Boosted throttle: {new_throttle}')
                    return new_throttle

            for angle, boost in self.negative_angles.items():
                if current_angle <= angle:
                    new_throttle = current_throttle + boost
                    print(f'Boosted throttle: {new_throttle}')
                    return new_throttle

        return current_throttle
