import time

from dronekit import connect, VehicleMode
from pymavlink import mavutil


# connects to the drone or the simulator, according to the input we give
def droneConnect(ip):
    if ip == "Yes":
        test = True
    else:
        test = False
    if test:
        print("Connected to the simulator, for help run the command\n<drone -h>")
        vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)
        print ("Connection complete")
        return vehicle
    else:
        print("Connecting to drone")
        return connect(ip, wait_ready=True)


# arms the drone
def arm(vehicle):
    #------
    if vehicle == "test":
        print("test arm")
        f = open('/home/drone/.local/lib/python2.7/site-packages/falconControl/drone/test.txt', 'w')
        f.write('test arm\n')
        return
    #------
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
    #------
    if vehicle == "test":
        print("test take of with")

        return
    #------
    if not vehicle.armed:
        print("Falcon needs to be armed first!!(drone -h for more information)")
        return
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


def takeoffDefault(vehicle):
    #------
    if vehicle == "test":
        print("test take of without")
        f = open('/home/drone/.local/lib/python2.7/site-packages/falconControl/drone/test.txt', 'w')
        f.write('test takeoff wt\n')
        return
    #------
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
    if not vehicle.armed:
        print("Falcon needs to be armed first!!(drone -h for more information)")
        return
    print("Taking off!")
    vehicle.simple_takeoff(1)  # Take off to target altitude
    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= 5 * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# given the directions and the time, drone will move accordingly
def move(vehicle, direction_x, direction_y, direction_z, duration):
    """
       Move vehicle in direction based on specified velocity vectors.

       This uses the SET_POSITION_TARGET_GLOBAL_INT command with type mask enabling only
       velocity components
       (http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_global_int).

       Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
       with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
       velocity persists until it is canceled. The code below should work on either version
       (sending the message multiple times does not cause problems).

       See the above link for information on the type_mask (0=enable, 1=ignore).
       At time of writing, acceleration and yaw bits are ignored.
       """
    #------
    if vehicle == "test":
        print("test move")
        return
    #------
    msg = vehicle.message_factory.set_position_target_global_int_encode(
        0,  # time_boot_ms (not used)
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,  # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0,  # lat_int - X Position in WGS84 frame in 1e7 * meters
        0,  # lon_int - Y Position in WGS84 frame in 1e7 * meters
        0,  # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
        # altitude above terrain if GLOBAL_TERRAIN_ALT_INT
        direction_x,  # X velocity in NED frame in m/s
        direction_y,  # Y velocity in NED frame in m/s
        direction_z,  # Z velocity in NED frame in m/s
        0, 0, 0,  # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    # send command to vehicle on 1 Hz cycle
    for x in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

# Land to current location
def land(vehicle):
    #------
    if vehicle == "test":
        print("test land")
        return
    #------
    vehicle.mode = VehicleMode("LAND")

# Horizontal rotate
def rotate(vehicle, direction, degree):
    """
        Send MAV_CMD_CONDITION_YAW message to point vehicle at a specified heading (in degrees).

        This method sets an absolute heading by default, but you can set the `relative` parameter
        to `True` to set yaw relative to the current yaw heading.

        By default the yaw of the vehicle will follow the direction of travel. After setting
        the yaw using this function there is no way to return to the default yaw "follow direction
        of travel" behaviour (https://github.com/diydrones/ardupilot/issues/2427)

        For more information see:
        http://copter.ardupilot.com/wiki/common-mavlink-mission-command-messages-mav_cmd/#mav_cmd_condition_yaw
        """
    #------
    if vehicle == "test":
        print("test rotate")
        return
    #------
    if direction[3:] == "right":
        dir = 1
    else:
        dir = -1
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
        0,  # confirmation
        degree,  # param 1, yaw in degrees
        0,  # param 2, yaw speed deg/s
        dir,  # param 3, direction -1 ccw, 1 cw
        1,  # param 4, relative offset 1, absolute angle 0
        0, 0, 0)  # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)