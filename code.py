# Helpful Links
# -------------
# Circuit Playground Tutorial: https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/neopixels
# Setting Up CircuitPython: https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries
# RGB Colors: https://www.chem.purdue.edu/gchelp/cchem/RGBColors/body_rgbcolors.html

from adafruit_circuitplayground.express import cpx
import time
import board
import busio
import adafruit_sgp30

#GLOBAL VARIABLES
FREQUENCY = 246
CO2_THRESHOLD = 500

# Make all of the pixels RED when someone touches
#              the A4 PAD on the Circuit Playground Express
# Touch A4 and see what happens.
# red green blue
# this is to test our idea
def touch():
    while True:
        print("here")
        if cpx.touch_A4:
            cpx.pixels.fill((200, 0, 0))
            print("touched A4")
        else:
            cpx.pixels.fill((0, 50, 0))

# Reads data frpom the Adafruit SGP30 sensor
# Example taken from https://learn.adafruit.com/adafruit-sgp30-gas-tvoc-eco2-mox-sensor?view=all#circuitpython-and-python-usage-6-12
def co2Sensor():
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
    print("SGP30 serial #", [hex(i) for i in sgp30.serial])

    sgp30.iaq_init()
    sgp30.set_iaq_baseline(0x8973, 0x8aae)

    elapsed_sec = 0
    #this loop is going to make all the lights go on before you can use the curcut playground
    for x in range(0, 9):
        cpx.pixels[x] = (50, 50, 0)
        time.sleep(2)
    # this is the thing that is allowing us to see our results
    while True:
        print('eCO2 = %d ppm \t TVOC = %d ppb' % (sgp30.eCO2, sgp30.TVOC))
        time.sleep(0.1)
        elapsed_sec += 1
        if elapsed_sec > 5:
            elapsed_sec = 0
            print("**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x" % (sgp30.baseline_eCO2, sgp30.baseline_TVOC))
        if sgp30.eCO2 >= CO2_THRESHOLD:
            cpx.pixels.fill((200, 0, 0))
            #playing a sound
            cpx.play_tone(FREQUENCY, 0.1)
        else:
            cpx.pixels.fill((20, 100, 0))
# calling the function
co2Sensor()