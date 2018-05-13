import gc

import machine
import pycom
import ubinascii
import utime
from machine import Pin
from machine import Timer

import lora
import sd
import sensor

# TODO synkronize every hour, for demo use button
# TODO possible time problem
# TODO send data lora
# TODO Format data to send
# TODO format data to save


# https://forum.pycom.io/topic/588/interrupt-button-debounce-with-long-short-press/12 used for button

pycom.heartbeat(False)
pycom.rgbled(0x7f00000)

tempList = []
lightList = []
timeList = []
limit = 3  # for testing
hourDivision = 3600000
fifteenMinutesDivision = hourDivision / 4
fiveMinutes = 300000
oneMinuteDivision = 60000


def restoreTempList():
    global tempList
    global lightList
    global timeList
    lightString = str(sd.getData(sd.light))
    print(lightString)
    tempString = str(sd.getData(sd.temperature))
    timeString = str(sd.getData(sd.time))
    tempList = tempString.split(",")
    lightList = lightString.split(",")
    print(str(lightList))
    timeList = timeString.split(",")


def updateLists():
    print("updateLists")
    global lightList
    global tempList
    global timeList
    lightValue = sensor.get_light()
    tempValue = sensor.get_temperature()
    timeValue = str(getTime())
    lightValue = (lightValue[0] + lightValue[1]) / 2
    lightList = updateList(lightList, lightValue)
    tempList = updateList(tempList, tempValue)
    timeList = updateList(timeList, timeValue)
    saveLists()

    # if len(lightList) == limit:
    #     doUpdate()
    doSleep()


def updateList(data: list, new: str):
    if data[0] == '': del data[:]
    if len(data) > 0:
        data = [new] + data
    else:
        data = [new]
    # while len(data) > limit:
    #     data.pop()
    return data


def saveLists():
    sd.save(','.join(map(str, lightList)), sd.light)
    sd.save(','.join(map(str, tempList)), sd.temperature)
    sd.save(','.join(map(str, timeList)), sd.time)


def getTime():
    return utime.time() * 1000  # Python yo


def doSleep(hasSend=False):  # TODO look at optimizing...
    time = getTime()  # change to hour for real testing
    timeLongDivision = fiveMinutes  # change to five for real testing
    timeShortDivision = oneMinuteDivision
    timePastShortDivision = (time + timeShortDivision) % timeShortDivision
    timeToNextShortDivision = ((time - timePastShortDivision) + timeShortDivision) - time

    timePastLongDivision = (time + timeLongDivision) % timeLongDivision
    timeToLongDivision = ((time - timePastLongDivision) + timeLongDivision) - time

    print(int(timeToNextShortDivision))
    print(int(timeToLongDivision))

    if int(timeToNextShortDivision) != int(timeToLongDivision):
        sleepForMs(int(timeToNextShortDivision))
    else:
        print("equal")
        if hasSend:
            sleepForMs(timeToNextShortDivision)  # sleep
        else:
            doUpdate()
            doSleep(True)


def sleepForMs(ms: int):
    print("sleep for " + str(ms))
    # machine.deepsleep(ms)


def updateData():
    temp = sensor.temp
    light = sensor.light
    tempList.append(temp)
    lightList.append(light)
    print(len(lightList))
    print(limit)
    # if len(lightList) == limit:
    #     doUpdate()


def clear():
    del tempList[:]
    del timeList[:]
    del lightList[:]


def doUpdate():
    sendToServer(buildString())
    clear()
    saveLists()


def buildString():
    lightString = '[' + ', '.join('"{0}"'.format(w) for w in lightList) + ']'
    tempString = '[' + ', '.join('"{0}"'.format(w) for w in tempList) + ']'
    timeString = '[' + ', '.join('"{0}"'.format(w) for w in timeList) + ']'
    print(lightString)
    return "{\"id\":\"" + getId() + "\",\"time\":" + lightString + ",\"temperature\":" + tempString + ", \"light\":" + timeString + "}"


def getId(): return str(ubinascii.hexlify(machine.unique_id()).upper()).replace("'", "").replace("b", "")


def sendToServer(dataString):
    print("init")
    print(dataString)
    lora.init()
    lora.send(dataString)


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
