class Threshold:
    def __init__(self, number):
        try:
            self.value = int(number)
            if self.value < 0:
                raise ValueError()
        except ValueError:
            raise ValueError('Threshold initialized with invalid value: {}'.format(number))
