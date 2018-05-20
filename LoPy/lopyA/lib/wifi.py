import machine
from network import WLAN


def init():
    wlan = WLAN(mode=WLAN.STA)
    nets = wlan.scan()
    for net in nets:
        if net.ssid == 'SDU-GUEST':
            print('Network found!')
            wlan.connect(net.ssid, auth=(net.sec, ''), timeout=5000)
            while not wlan.isconnected():
                machine.idle()  # save power while waiting
            print('WLAN connection succeeded!')
            break
