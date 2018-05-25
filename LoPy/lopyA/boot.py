import machine
import pycom
import utime
from network import WLAN

pycom.heartbeat(False)

pycom.rgbled(0x7f00000)


def setTime():
    rtc = machine.RTC()
    rtc.ntp_sync("pool.ntp.org")
    while not rtc.synced():
        utime.sleep_ms(50)
    print(utime.time())
    print(rtc.now())


print(int(utime.time() * 1000))

if utime.time() < 1000:
    wlan = WLAN(mode=WLAN.STA)
    nets = wlan.scan()
    for net in nets:
        if net.ssid == 'SDU-GUEST':
            print('Network found!')
            wlan.connect(net.ssid, auth=(net.sec, ''), timeout=5000)
            while not wlan.isconnected():
                machine.idle()  # save power while waiting
            print('WLAN connection succeeded!')
            setTime()
            wlan.deinit()
            break
