from SI7006A20 import SI7006A20 as TempSensor

tsensor = TempSensor()

def get_temperature():
    return { 'temperature' : tsensor.temperature(), 'humidity' : tsensor.humidity()}
