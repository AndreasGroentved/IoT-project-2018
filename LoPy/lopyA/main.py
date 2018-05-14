import gc
import socket

import machine
import pycom
import utime
from machine import Pin
from machine import Timer
from network import LoRa

import sd
import sensor

# TODO synkronize every hour, for demo use button
# TODO save data
# TODO retrieve data
# TODO send data lora
# TODO Format data to send
# TODO format data to save


# https://forum.pycom.io/topic/588/interrupt-button-debounce-with-long-short-press/12 used for button

pycom.heartbeat(False)
pycom.rgbled(0x7f00000)

tempList = []
lightList = []
timeList = []
limit = 5  # for testing
hourDivision = 3600000
fiveMinutes = 300000


def restoreTempList():
    global tempList
    global lightList
    global timeList
    lightString = str(sd.getData(sd.light))
    tempString = str(sd.getData(sd.temperature))
    timeString = str(sd.getData(sd.time))
    tempList = tempString.split(",")
    lightList = lightString.split(",")
    timeList = timeString.split(",")


def updateLists():
    global lightList
    global tempList
    lightValue = sensor.get_light()
    tempValue = sensor.get_temperature()
    lightValue = (lightValue[0] + lightValue[1])
    lightList = updateList(lightList, lightValue)
    tempList = updateList(tempList, tempValue)
    saveLists()


def updateList(data: list, new: str):
    data = [new] + data
    while len(data) > limit:
        data.pop()
    return data


def saveLists():
    sd.save(','.join(map(str, lightList)), sd.light)
    sd.save(','.join(map(str, tempList)), sd.temperature)
    sd.save(','.join(map(str, timeList)), sd.time)


def getTime():
    return int(utime.time() * 1000)  # Python yo


def timeToNextHour(currentTime):
    return hourDivision / currentTime


def getTimeToNextFive():
    pass


def updateData():
    temp = sensor.temp
    light = sensor.light
    tempList.append(temp)
    lightList.append(light)

    # machine.deepsleep(5000)


def doUpdate():
    sendLora(buildString())


def buildString():
    lightString = '[' + ', '.join('"{0}"'.format(w) for w in lightList) + ']'
    tempString = '[' + ', '.join('"{0}"'.format(w) for w in tempList) + ']'
    timeString = '[' + ', '.join('"{0}"'.format(w) for w in timeList) + ']'
    return "{'id':'" + getId() + "','time':[" + lightString + "],'temperature':[" + tempString + "], 'light':[" + timeString + "]}"


def getId(): return machine.unique_id()


def sendLora(dataString):
    lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    s.send(dataString)


def initOperations():
    sd.init()
    restoreTempList()
    updateLists()


initOperations()

butms = 0
butup = 0

chrono = Timer.Chrono()
timer = Timer.Alarm(None, 1.5, periodic=False)

btn = machine.Pin('P14', mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)


def long_press_handler(alarm):
    print("****** LONG PRESS HANDLER ******")
    machine.deepsleep(1)


def single_press_handler():
    print("****** BUTTON PRESSED ******")


def btn_press_detected(arg):
    global chrono, timer
    try:
        val = btn()
        if 0 == val:
            chrono.reset()
            chrono.start()
            timer.callback(long_press_handler)
        else:
            timer.callback(None)
            chrono.stop()
            t = chrono.read_ms()
            if (t > 60) & (t < 200):
                single_press_handler()
    finally:
        gc.collect()


btn.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING, btn_press_detected)
