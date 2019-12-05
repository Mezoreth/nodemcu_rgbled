# This file is executed on every boot (including wake-boot from deepsleep)

import gc
gc.collect()

import network

ssid = 'nombre del ssid'
password = 'password'

ap_if = network.WLAN(network.STA_IF)
ap_if.active(True)
ap_if.connect(ssid, password)

while ap_if.isconnected() == False:
    pass


print('Connection successful')
print(ap_if.ifconfig())
