import machine
import pycom
import ubinascii
import utime

import bluetooth
import lora
import requests
import sd
import sensor
import wifi

pycom.heartbeat(False)
pycom.rgbled(0x7f00000)

tempList = []
lightList = []
timeList = []
hourDivision = 3600000
fifteenMinutesDivision = 900000
fiveMinutes = 300000
oneMinuteDivision = 60000


def restoreTempList():
    global tempList
    global lightList
    global timeList
    lightString = ''  # str(sd.getData(sd.light))
    tempString = ''  # str(sd.getData(sd.temperature))
    timeString = ''  # str(sd.getData(sd.time))
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
    doUpdate()
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
    # sd.save(','.join(map(str, lightList)), sd.light)
    # sd.save(','.join(map(str, tempList)), sd.temperature)
    # sd.save(','.join(map(str, timeList)), sd.time)
    pass


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

    sleepForMs(timeToNextShortDivision)


def sleepForMs(ms: int):
    print("sleep for " + str(ms))
    machine.deepsleep(ms)


def sendOverWifi(dataStringList: list):
    print(str(dataStringList))
    print(constructDataString(dataStringList))
    json = buildJSON(constructDataString(dataStringList))
    print(json)
    wifi.init()

    requests.request('POST', 'https://iot-web-app-2018.herokuapp.com/temperature', json, None,
                     {"Content-Type": "application/json"})


def buildJSON(data):
    arr = data.split(":")
    out = "{\"id\":" + "\"" + arr[0] + "\","
    out += "\"light\":[" + arr[1] + "],"
    out += "\"temp\":[" + arr[2] + "],"
    out += "\"time\":" + buildTimeJson(arr[3])
    out += "}"
    out = out.replace("'", "\"")
    print(out)
    return out


def buildTimeJson(string):
    w = str(string)
    if "," in w:
        arr = w.split(",")
        print(str(arr))
        return '[' + ', '.join(
            '"{0}"'.format("152" + str(q).replace("'", "").replace("\"", "") + "000") for q in arr) + ']'
    else:
        return "[\"" + "152" + str(w).replace("'", "").replace("\"", "") + "000" + "\"]"


def clear():
    del tempList[:]
    del timeList[:]
    del lightList[:]


def doUpdate():
    clear()
    saveLists()


def getNull(data):
    if str(data) == "" or str(data) == " ":
        return "0"
    else:
        return str(data)


def getId(): return str(ubinascii.hexlify(machine.unique_id()).upper()).replace("'", "").replace("b", "")


def constructDataString(data):
    print(len(data))
    lengthOtType = int(int(len(data) + 1) / 4)
    print(str(lengthOtType))
    # Todo hardcoded id - nono
    idString = "b"
    index = 0
    lightString = ','.join('"{0}"'.format(w) for w in data[index:lengthOtType])
    index += lengthOtType
    tempString = ','.join('"{0}"'.format(str(w)) for w in data[index:lengthOtType + index])
    index += lengthOtType
    timeString = ','.join('"{0}"'.format(w) for w in data[index:lengthOtType + index])
    return idString + ":" + tempString + ":" + lightString + ":" + timeString


def sendToServerLora(dataString):
    print(str(dataString))
    data = constructDataString(dataString)
    lora.init()
    lora.send(data)


def checkBluetooth():  # scan for nodes advertising data and choose how to send it
    try:
        value = bluetooth.scan(15)
        print("value " + str(value))
        print("len " + str(len(value)))
        if not value:
            return
        wifi = shouldUseWifi(value)
        if wifi:
            sendOverWifi(value)
        else:
            sendToServerLora(value)
    except Exception as e:
        print("Error " + str(e))
    doSleep(True)


def shouldUseWifi(data: list): return len(data) > 4


def initOperations():
    sd.init()
    restoreTempList()
    checkBluetooth()
    updateLists()


initOperations()
