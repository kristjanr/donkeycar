class TurnBoost():
    '''
    This part will apply a thrust during turns where angles are extreme enough to cause the slowdown of the car.
    This is to help in turning when the car slows down because of friction or voltage drop caused by servo usage.
    This has two goals:
    1. To maintain a constant actual speed of the car throughout the track
    2. Avoid it stopping completely during tight and long turns whend driving slowly.
    '''

    def __init__(self, config: dict):
        self.positive_angles = sorted([(angle, boost) for angle, boost in config.items() if angle > 0], reverse=True)
        self.negative_angles = sorted([(angle, boost) for angle, boost in config.items() if angle < 0])
        self.enabled = False
        self.counter = 0

    def toggle(self):
        self.enabled = not self.enabled
        print(f'TurnBoost is {"enabled" if self.enabled else "disabled"}.')

    def run(self, mode, current_angle, current_throttle):
        self.counter += 1
        if mode == "user" and self.enabled:
            for angle, boost in self.positive_angles:
                if current_angle >= angle:
                    new_throttle = min(1.0, current_throttle + boost)
                    if self.counter % 5 == 0:
                        print(str.format("Tight right turn (more than {:.2f}). Boosted throttle: {:.2f}", angle, new_throttle))
                    return new_throttle

            for angle, boost in self.negative_angles:
                if current_angle <= angle:
                    new_throttle = min(1.0, current_throttle + boost)
                    if self.counter % 5 == 0:
                        print(str.format("Tight left turn (less than {:.2f}). Boosted throttle: {:.2f}", angle, new_throttle))
                    return new_throttle

        return current_throttle
