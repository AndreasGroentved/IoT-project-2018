import machine
import time
import utime
from network import WLAN
wlan = WLAN(mode=WLAN.STA)


def setTime():
    from machine import RTC
    rtc = machine.RTC()
    rtc.ntp_sync("pool.ntp.org")
    utime.sleep_ms(750)
    print(rtc.now())

nets = wlan.scan()
for net in nets:
    if net.ssid == 'SDU-GUEST':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, ''), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        setTime()
        break


