
import utime
from network import Bluetooth

# starting point in https://docs.pycom.io/chapter/firmwareapi/pycom/network/bluetooth/

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
        utime.sleep(0.05)
        advs = bt.get_advertisements()

        if advs is None:
            bt.stop_scan()
            continue

        for adv in advs:
            if adv and bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'Loy':
                con = False
                conn = None
                try:
                    print("try?")
                    if con is False:   conn = bt.connect(adv.mac)
                    services = conn.services()
                    con = True
                    for service in services:
                        chars = service.characteristics()
                        for char in chars:
                            if char.properties() & Bluetooth.PROP_READ:
                                if type(service.uuid()) == bytes:
                                    this = str(char.read().decode('utf-8'))
                                    while str(this) != str("i") and str(this) != "":
                                        print("this " + this)
                                        out.append(this)
                                        this = str(char.read().decode('utf-8'))

                                    if this == "":
                                        if conn is not None: conn.disconnect()
                                        con = False
                                        return out

                    if conn is not None: conn.disconnect()
                    con = False
                except Exception as inst:
                    last = utime.time()
                    print("failed is con " + str(con))
                    print(str(inst))
                    if conn is not None: conn.disconnect()
                break
