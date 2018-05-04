import pycom
import time
pycom.heartbeat(False)
for cycles in range(10):  # stop after 10 cycles
    pycom.rgbled(0x007f00)  # green
    time.sleep(5)
    pycom.rgbled(0x7f7f00)  # yellow
    time.sleep(1.5)
    pycom.rgbled(0x7f0000)  # red
    time.sleep(4)
    print("light")

""" LoPy LoRaWAN Nano Gateway example usage """

import config
from nanogateway import NanoGateway

if __name__ == '__main__':
    nanogw = NanoGateway(
        id=config.GATEWAY_ID,
        frequency=config.LORA_FREQUENCY,
        datarate=config.LORA_GW_DR,
        ssid=config.WIFI_SSID,
        password=config.WIFI_PASS,
        server=config.SERVER,
        port=config.PORT,
        ntp_server=config.NTP,
        ntp_period=config.NTP_PERIOD_S
        )

    nanogw.start()
    nanogw._log('You may now press ENTER to enter the REPL')
    input()
