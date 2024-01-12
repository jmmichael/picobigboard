#logbme280_threaded.py
from machine import Pin, I2C
from time import sleep
import bme280
import utime
#import led_w
import machine
import _thread
import network
import socket
import time
import struct
from machine import Pin
import simple_ntp
from secret import ssid, password



spi_sck=machine.Pin(2)
spi_tx=machine.Pin(3)
spi_rx=machine.Pin(4)
spi=machine.SPI(0,baudrate=100000,sck=spi_sck, mosi=spi_tx, miso=spi_rx)

#initialise I2C
i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)

led = machine.Pin("LED", machine.Pin.OUT)


'''
led = Pin("LED", Pin.OUT)

hour_pins = [machine.Pin(0), machine.Pin(1), machine.Pin(2), machine.Pin(3), machine.Pin(4)]
minute_pins = [machine.Pin(5), machine.Pin(6), machine.Pin(7), machine.Pin(8), machine.Pin(9)]
second_pins = [machine.Pin(10), machine.Pin(11), machine.Pin(12), machine.Pin(13), machine.Pin(14)]


led = machine.Pin("LED", machine.Pin.OUT)
'''
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

led.on()
simple_ntp.set_time()
print(time.localtime())
led.off()



# define function to handle the first core (Core 1)
def first_core_function():
    while True:
        bme = bme280.BME280(i2c=i2c)
        temp = bme.values[0]
        pressure = bme.values[1]
        humidity = bme.values[2]
        reading = 'Temperature: ' + temp + '. Humidity: ' + humidity + '. Pressure: ' + pressure
        shortreading = ','+temp +','+ humidity + ','+pressure
        print(reading)
        data_file = open("MyData.txt","a") 
        data_file.write(str(utime.localtime()) +shortreading + '\n')
        data_file.close()
        print("Wrote data to file\n")    
        led.toggle()
        sleep(6)
    
# define function to handle the second core (Core 2)
def second_core_function():
    while True:
        bme = bme280.BME280(i2c=i2c)
        temp = bme.values[0]          
        spi.write('\x7C')
        spi.write('\x2D')
        out_string = "Temp: " +str(temp)
        spi.write(out_string)
        utime.sleep(2)
# start new thread 
_thread.start_new_thread(second_core_function, ())

# main loop on core 1
while True:
# execute the first core function
    first_core_function()
