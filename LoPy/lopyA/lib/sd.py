import os

from machine import SD


def init():
    sd = SD()
    os.mount(sd, '/sd')
    print(os.listdir('/sd'))


light = 0
time = 1
temperature = 2


def save(dataString, dataType):
    path = getPath(dataType)
    f = open(path, 'w')
    print("writing " + path + ", data: " + dataString)
    f.write(dataString)
    f.close()


def getPath(dataType):
    path = ""
    if dataType == 0:
        path = "light"
    elif dataType == 1:
        path = "time"
    elif dataType == 2:
        path = "temp"
    path = '/sd/' + path + '.txt'
    return path


def getData(dataType):
    path = getPath(dataType)
    f = open(path, 'r')
    out = f.readall()
    f.close()
    return out
