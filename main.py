from gpiozero import PWMLED, DistanceSensor
import time
from signal import signal, SIGTERM, SIGHUP
import logging

led = PWMLED(17)
ultrasonic = DistanceSensor(
    echo=27, trigger=22, max_distance=1.00, threshold_distance=0.1)

f = open("errorlog.txt", "a")

def sig_terminate()
    f.write("Debug: Terminate Signal received from the command line.")
    f.close()
    print("Debug: Terminate Signal received from the command line.")
    exit(1)

def sig_hangup():
        
    f.write("Debug: Terminal got disconnected.")
    f.close()
    exit(1)

try:
    signal(SIGTERM, sig_terminate)
    signal(SIGHUP, sig_hangup)
    led.off()
    while True:
        distance = ultrasonic.value
        print(f"Distance => {distance: 1.2f} m")
        duty_cycle = round(1.0 - distance, 1)
        if duty_cycle < 0:
            duty_cycle = 0.0
        led.value = duty_cycle
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Program came to an end: Keyboard Interrupt (Ctrl + C pressed).")

finally:
    ultrasonic.close()
