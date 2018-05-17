from network import Bluetooth




def init(callback):
    bt = Bluetooth()
    bt.set_advertisement(name='LoPy', service_uuid=b'1234567890123456')
    bt.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=callback)
    bt.advertise(True)
