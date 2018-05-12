import binascii
import socket
import time

from network import LoRa

import config

global s


def init():
    global s
    # initialize LoRa in LORAWAN mode.
    # Please pick the region that matches where you are using the device:
    # Asia = LoRa.AS923
    # Australia = LoRa.AU915
    Europe = LoRa.EU868
    # United States = LoRa.US915
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

    # create an OTA authentication params
    # dev_eui = binascii.unhexlify('30AEA4FFFE505654')
    dev_eui = binascii.unhexlify('3AAEA4FFFE505654')
    app_eui = binascii.unhexlify('70B3D57ED000BDA0')
    # app_key = binascii.unhexlify('6D08E6C2C4237B3A1D223404713DF335')
    app_key = binascii.unhexlify('705DFC1AF37D90FB858F510EAFAAAE14')

    # set the 3 default channels to the same frequency (must be before sending the OTAA join request)
    lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
    lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
    lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

    # join a network using OTAA
    lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=config.LORA_NODE_DR)

    # wait until the module has joined the network
    while not lora.has_joined():
        time.sleep(2.5)
        print('Not joined yet...')

    print('Joined')

    # remove all the non-default channels
    for i in range(3, 16):
        lora.remove_channel(i)

    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

    # make the socket blocking
    s.setblocking(False)


def send(data):
    s.send(data)
