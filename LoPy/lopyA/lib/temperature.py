import SI7006A20

tsensor = SI7006A20.SI7006A20()


def get_temperature():
    return Temp(tsensor.temperature(), tsensor.humidity())


class Temp:
    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity
