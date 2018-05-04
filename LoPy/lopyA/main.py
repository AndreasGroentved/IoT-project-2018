import time
import pycom
import utime
from machine import RTC

import requests
import temperature

""" LoPy LoRaWAN Nano Gateway example usage """

import config
from nanogateway import NanoGateway

if __name__ == '__main__':
    nanogw = NanoGateway(
        id=config.GATEWAY_ID,
        frequency=config.LORA_FREQUENCY,
        datarate=config.LORA_GW_DR,
        ssid=config.WIFI_SSID,
        password=config.WIFI_PASS,
        server=config.SERVER,
        port=config.PORT
        )

    nanogw.start()
    print('Started!')
    #nanogw._log('You may now press ENTER to enter the REPL')
    #input()


def getTime():
    return int(utime.time()) * 1000  # Python yo


def postTemp(temp, time=None):
    if time is None:
        currentTime = getTime()
    else:
        currentTime = time
    print('{"temperature":' + str(temp) + ',"time":' + str(currentTime) + '}')
    return requests.request('POST', 'https://iot-web-app-2018.herokuapp.com/temperature',
                            '{"temperature":' + str(temp) + ',"time":' + str(currentTime) + '}', None,
                            {"Content-Type": "application/json"}).text


def getTemps():
    return requests.request('GET', 'https://iot-web-app-2018.herokuapp.com/temperature', None,
                            {"Content-Type": "application/json"}).text


# temperatures = list()

'''
while True:
    thetemp = temperature.get_temperature()
    #   temperatures.append(thetemp)
    # print(postTemp(thetemp.temperature))
    print(thetemp.temperature)
    time.sleep(1)
'''

# for cycles in range(10):  # stop after 10 cycles
#     pycom.rgbled(0x007f00)  # green
#     time.sleep(5)
#     pycom.rgbled(0x7f7f00)  # yellow
#     time.sleep(1.5)
#     pycom.rgbled(0x7f0000)  # red
#     time.sleep(4)
#     print("light")
