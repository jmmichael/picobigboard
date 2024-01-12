#file:///home/pi/Bookshelf/RPi_PiPico_Digital_v10.pdf, pp122
import machine
import utime
spi_sck=machine.Pin(2)
spi_tx=machine.Pin(3)
spi_rx=machine.Pin(4)
spi=machine.SPI(0,baudrate=100000,sck=spi_sck, mosi=spi_tx, miso=spi_rx)
adc = machine.ADC(4)
conversion_factor = 3.3 / (65535)
while True:
    reading = adc.read_u16() * conversion_factor
    temperature = 25 - (reading - 0.706)/0.001721
    spi.write('\x7C')
    spi.write('\x2D')
    out_string = "Temp: " +str(temperature)
    spi.write(out_string)
    utime.sleep(2)
    print (temperature)