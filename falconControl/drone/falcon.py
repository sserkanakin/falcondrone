import time

from dronekit import connect, VehicleMode


# connects to the drone or the simulator, according to the input we give
def droneConnect(ip):
    if ip == "Yes":
        test = True
    if test:
        print("Connected to the simulator, for help run the command\n<drone -h>")
        return connect('tcp:127.0.0.1:5760', wait_ready=True)
    else:
        return connect(ip, wait_ready=True)


# arms the drone
def arm(vehicle):
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    print ("Falcon is armed, ready to take off!")


def takeoff(vehicle, aTargetAltitude):
    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude
    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)
def takeoff(vehicle):
  print("takeoff without")
def move(vehicle, direction, amount):
  print ("move")




