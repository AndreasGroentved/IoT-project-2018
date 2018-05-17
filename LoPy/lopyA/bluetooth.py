import time
from network import Bluetooth

bt = Bluetooth()

def scan():
    bt.start_scan(5)
    while bt.isscanning():
        adv = bt.get_adv()
        values = {}
        if adv and bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'Loy':
            try:
                conn = bt.connect(adv.mac)
                services = conn.services()
                for service in services:
                    time.sleep(0.050)
                    if type(service.uuid()) == bytes:
                        print('Reading chars from service 1 = {}'.format(service.uuid()))
                    else:
                        print('Reading chars from service 2 = %x' % service.uuid())
                    chars = service.characteristics()
                    for char in chars:
                        if (char.properties() & Bluetooth.PROP_READ):
                            print('char {} value = {}'.format(char.uuid(), char.read()))
                            if type(service.uuid()) == bytes:
                                values[char.uuid().decode('utf-8')[:2]] = char.read().decode('utf-8')
                conn.disconnect()
            except:
                print("Error while connecting or reading from the BLE device")
                conn.disconnect()
                break
        else:
            time.sleep(1)
    return values
