from gpiozero import PWMLED, DistanceSensor
import time
from signal import signal, SIGTERM, SIGHUP


led = PWMLED(12)
ultrasonic = DistanceSensor(
    echo=13, trigger=19, max_distance=0.35, threshold_distance=0.05)

f = open("errorlog.txt", "a")

d = open("distance.txt", "a")

def sig_terminate():
    f.write("Debug: Terminate Signal received from the command line. \n")
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
        distance = ultrasonic.value * 0.35
        print(f"Distance => {distance: 1.2f} m")
        
        d.write(f"{time.asctime(time.localtime(time.time()))} Distance => {distance: 1.2f} m")
        duty_cycle = round(1.0 - distance/0.35, 1)
        if duty_cycle < 0:
            duty_cycle = 0.0
        led.value = duty_cycle
        d.write(f" Led value: {led.value} \n")
        time.sleep(0.5)
except KeyboardInterrupt as kb:
    f.write(f"{time.asctime(time.localtime(time.time()))} {str(kb)} Program came to an end: (Ctrl + C pressed).\n")
    print("Program came to an end: Keyboard Interrupt (Ctrl + C pressed).")
    d.close()
    f.close()
    
finally:
    led.off()
    ultrasonic.close()
