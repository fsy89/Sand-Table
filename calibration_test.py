import RPi.GPIO as GPIO
from DRV8825 import DRV8825
from time import sleep

M_Rot = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
M_Lin = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))

outer_switch = 5
inner_switch = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(outer_switch, GPIO.IN)
GPIO.setup(inner_switch, GPIO.IN)

delay = 1 / 1000
pos = 0
center_to_min = 20
outer_to_max = 20

calibrated = False

def run_MRot(stepdelay):
    while not calibrated:
            self.digital_write(self.step_pin, True)
            time.sleep(stepdelay)
            self.digital_write(self.step_pin, False)
            time.sleep(stepdelay)

def calibrate():
    while not calibrated:
        minPos = M_Lin.Turn(Dir='backward', limit_switch=inner_switch, stepdelay=delay)
        maxPos = M_Lin.Turn(Dir='forward', limit_switch=outer_switch, stepdelay=delay) + minPos

        positions = (minPos, maxPos)
        print(positions)
        totalDist = maxPos - minPos - center_to_min - outer_to_max
        print ("Travel Distance: " + str(totalDist))

        sleep(2)

        test_inner = M_Lin.TurnStep_test(Dir='backward', steps=totalDist + outer_to_max, limit_switch=inner_switch, stepdelay=delay)
        minPos = 0
        sleep(2)
        test_outer = M_Lin.TurnStep_test(Dir='forward', steps=totalDist, limit_switch=outer_switch, stepdelay=delay)
        maxPos = totalDist
        if test_inner and test_outer:
            calibrated = True
        else:
            print("Calibration Failed! Trying again...")
    print("Calibration Passed!")    

def stop_program(threading_event):
    # threading_event.set()
    MRot.join()
    MLin.join()
    print("\nMotors stopped")
    M_Rot.Stop()
    M_Lin.Stop()
    GPIO.cleanup()
    print("Exiting...")
    exit()

try:
    threading_event = threading.Event()
    
    MRot = threading.Thread(target=run_MRot, args=delay,)
    MLin = threading.Thread(target=calibrate)

    print("...")
    MRot.start()
    MLin.start()

    MRot.join()
    MLin.join()
except KeyboardInterrupt:
    stop_program(threading_event)