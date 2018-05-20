import gc

import machine
import pycom
import ubinascii
import utime
from machine import Pin
from machine import Timer

import bluetooth
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
hourDivision = 3600000
fifteenMinutesDivision = 900000
fiveMinutes = 300000
oneMinuteDivision = 60000
bluetoothReceiver = "SOMEMACADDRESS"  # TODO find mac adress


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
    global timeList
    lightValue = sensor.get_light()
    tempValue = sensor.get_temperature()
    timeValue = str(getTime())
    lightValue = (lightValue[0] + lightValue[1]) / 2  # TODO fast solution -> find better
    lightList = updateList(lightList, lightValue)
    tempList = updateList(tempList, tempValue)
    timeList = updateTime(timeList, timeValue)
    saveLists()
    # doUpdate()
    # sendToServer(buildString())
    assessSituation()


def assessSituation():
    if float(tempList[0]) > float(30):
        doUpdate(lightList[:1], tempList[:1], timeList[:1], False)
    else:
        doSleep()


def updateList(data: list, new: float):
    if data[0] == '': del data[:]
    if len(data) > 0:
        data = ["%.1f" % round(new, 1)] + data
    else:
        data = ["%.1f" % round(new, 1)]
    return data


def updateTime(data: list, new: str):
    if data[0] == '': del data[:]
    if len(data) > 0:
        data = [new] + data
    else:
        data = [new]
    return data


def saveLists():
    sd.save(','.join(map(str, lightList)), sd.light)
    sd.save(','.join(map(str, tempList)), sd.temperature)
    sd.save(','.join(map(str, timeList)), sd.time)


def getTime():
    return utime.time() * 1000  # Python yo


def doSleep(hasSend=False):  # TODO look at optimizing...
    time = getTime()
    timeLongDivision = fiveMinutes  # change to hour for real testing
    timeShortDivision = oneMinuteDivision  # change to five for real testing
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
            doUpdate(lightList, tempList, timeList, True)
            # clear()
            # doSleep(True)


def sleepForMs(ms: int):
    print("sleep for " + str(ms))
    machine.deepsleep(ms)


def clear():
    del tempList[:]
    del timeList[:]
    del lightList[:]
    saveLists()


def doUpdate(lightList, tempList, timeList, clear):
    sendToServer(buildString(lightList, tempList, timeList), clear)


def buildString(lightList, tempList, timeList):
    lightString = ', '.join("{0}".format(getNull(w)) for w in lightList)
    tempString = ', '.join("{0}".format(w) for w in tempList)
    timeString = ', '.join(
        "{0}".format(str(int(int(w) / 1000))[3:]) for w in timeList)  # look at type
    ret = "b" + ":" + lightString + ":" + tempString + ":" + timeString

    print(ret)
    return ret


def getNull(data):
    if str(data) == "" or str(data) == " ":
        return "0"
    else:
        return str(data)


def getId(): return str(ubinascii.hexlify(machine.unique_id()).upper()).replace("'", "").replace("b", "")


def sendToServer(dataString, clear):
    print(dataString)
    toSend = bluetooth.startSending([tempList, lightList, timeList, ["b"]], afterBLEUpdate, clear)
    # lora.init()
    # lora.send(dataString)


def afterBLEUpdate(clearrr):
    print("after")
    if clearrr: clear()
    doSleep(True)


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
    # sendToServer(buildString())


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
