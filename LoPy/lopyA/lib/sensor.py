from LTR329ALS01 import LTR329ALS01 as LightSensor
from SI7006A20 import SI7006A20 as TempSensor

temp = TempSensor()
light = LightSensor()


def get_temperature():
    return temp.temperature()


def get_light():
    return light.light()
