#Files from https://drive.google.com/drive/u/0/folders/11NniRrdWbp-h6SOk2OLFI4mkFYe6gYgr
#https://www.youtube.com/playlist?list=PLrJp3bvNEFaWtttqk0eVx2NZ97cG8Y8-x
# import the required libraries
from machine import Pin
import _thread
import utime

# declare pins for leds 
red_led = Pin(20, mode = Pin.OUT, value = 0)
yellow_led = Pin(21, mode = Pin.OUT, value = 0)

# define function to handle the first core (Core 1)
def first_core_function():
    yellow_led.toggle()
    utime.sleep(5)
    yellow_led.toggle()
    utime.sleep(5)
    print("\n","Hello There ! i am the FIRST CORE","\n")
     #Open, Write, Close a datafile
    data_file = open("MyData.txt","a")
    data_file.write('write to file'+'\n')
    data_file.close()
    print("Wrote data to file")
    

# define function to handle the second core (Core 2)
def second_core_function():
    while True:
        red_led.toggle()
        utime.sleep(1)
        red_led.toggle()
        utime.sleep(1)
        print("Hello There ! i am the SECOND CORE")                

# start new thread 
_thread.start_new_thread(second_core_function, ())

# main loop on core 1
while True:
# execute the first core function
    first_core_function()