import time

import utime
from network import Bluetooth

bt = Bluetooth()

global last


def scan(maxTime):
    print("scanning " + str(bt.isscanning()))
    out = []
    global last
    last = utime.time()
    while True:
        if utime.time() - last > maxTime: return []

        if not bt.isscanning():
            bt.start_scan(-1)
        time.sleep(0.05)
        advs = bt.get_advertisements()

        if advs is None:
            bt.stop_scan()
            continue

        for adv in advs:
            if adv and bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'Loy':
                # print("if?")
                con = False
                conn = None
                try:
                    print("try?")
                    if con is False:   conn = bt.connect(adv.mac)
                    services = conn.services()
                    con = True
                    current = ""
                    for service in services:
                        #time.sleep(0.050)
                        chars = service.characteristics()
                        for char in chars:
                            if char.properties() & Bluetooth.PROP_READ:
                                if type(service.uuid()) == bytes:
                                    this = str(char.read().decode('utf-8'))
                                    print(this)
                                    while str(this) != str("i") and str(this) != "":
                                        print("this " + this)
                                        # out += this
                                        out.append(this)
                                        this = str(char.read().decode('utf-8'))
                                    # if this != "i":      current += this
                                    # print("cur " + current)
                                    if this == "":
                                        if conn is not None: conn.disconnect()
                                        con = False
                                        return out
                                    # out +=
                                    #     if this == "":
                                    #         print("stop!")
                                    #         return out  # values
                                    #
                                    # else:
                                    # print("not bytes " + str(char.read()))

                    # print("out success " + out)

                    if conn is not None: conn.disconnect()
                    con = False
                    print("dont stop")
                except Exception as inst:
                    last = utime.time()
                    print("failed is con " + str(con))
                    print(str(inst))
                    if conn is not None: conn.disconnect()
                    print("failed")
                break
            else:
                time.sleep(0.1)
