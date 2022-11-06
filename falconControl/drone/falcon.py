from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil  # Needed for command message definitions
import time
import math

drone = ""
# connects to the drone or the simulator, according to the input we give
def droneConnect(connection_string, baud):
    print("Connecting to drone")
    vehicle = connect(connection_string, baud=baud, wait_ready=True)
    drone = vehicle
    print("connected")
    vehicle.airspeed = 3
    return vehicle


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
    arm(vehicle)
    if not vehicle.armed:
        print("Falcon needs to be armed first")
        return
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


# given the directions and the time, drone will move accordingly
def move_horizontal(vehicle, direction, metres, gotoFunction = drone.simple_goto):
    yaw = vehicle.attitude.yaw
    if 0 <= yaw <= 90:
        dir_comp = "N"
    elif 90 < yaw <= 180:
        dir_comp = "E"
    elif 180 < yaw <= 270:
        dir_comp = "S"
    else:
        dir_comp = "W"
    if (direction == "f" and dir_comp == "N") or (direction == "r" and dir_comp == "W") or (direction == "l" and dir_comp == "E") or (direction == "b" and dir_comp == "S"):
        d_north = metres
        d_east = 0
    elif (direction == "f" and dir_comp == "S") or (direction == "r" and dir_comp == "E") or (direction == "l" and dir_comp == "W") or (direction == "b" and dir_comp == "N"):
        d_north = metres * -1
        d_east = 0
    elif (direction == "f" and dir_comp == "E") or (direction == "r" and dir_comp == "N") or (direction == "l" and dir_comp == "S") or (direction == "b" and dir_comp == "W"):
        d_north = 0
        d_east = metres
    else:
        d_north = 0
        d_east = metres * -1
    current_location = vehicle.location.global_relative_frame
    target_location = get_location_metres(current_location, d_north, d_east)
    target_distance = get_distance_metres(current_location, target_location)
    gotoFunction(target_location)

    # print "DEBUG: targetLocation: %s" % targetLocation
    # print "DEBUG: targetLocation: %s" % targetDistance

    while vehicle.mode.name == "GUIDED":  # Stop action if we are no longer in guided mode.
        # print "DEBUG: mode: %s" % vehicle.mode.name
        remainingDistance = get_distance_metres(vehicle.location.global_relative_frame, target_location)
        print("Distance to target: ", remainingDistance)
        if remainingDistance <= target_distance * 0.01:  # Just below target, in case of undershoot.
            print("Reached target")
            break
        time.sleep(2)


def move_vertical(vehicle, movement, duration):
    msg = vehicle.message_factory.set_position_target_global_int_encode(
        0,  # time_boot_ms (not used)
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,  # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0,  # lat_int - X Position in WGS84 frame in 1e7 * meters
        0,  # lon_int - Y Position in WGS84 frame in 1e7 * meters
        0,  # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
        # altitude above terrain if GLOBAL_TERRAIN_ALT_INT
        0,  # X velocity in NED frame in m/s
        0,  # Y velocity in NED frame in m/s
        movement,  # Z velocity in NED frame in m/s
        0, 0, 0,  # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    # send command to vehicle on 1 Hz cycle
    for x in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)


    # Land to current location
def land(vehicle):
    vehicle.mode = VehicleMode("LAND")


def rotate(vehicle, direction):
    if direction == "r":
        rot_dir = 1
    else:
        rot_dir = -1
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
        0,  # confirmation
        90,  # param 1, yaw in degrees
        0,  # param 2, yaw speed deg/s
        rot_dir,  # param 3, direction -1 ccw, 1 cw
        1,  # param 4, relative offset 1, absolute angle 0
        0, 0, 0)  # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)


def get_location_metres(original_location, d_north, d_east):
    earth_radius = 6378137.0  # Radius of "spherical" earth
    # Coordinate offsets in radians
    dLat = d_north / earth_radius
    dLon = d_east / (earth_radius * math.cos(math.pi * original_location.lat / 180))

    # New position in decimal degrees
    new_lat = original_location.lat + (dLat * 180 / math.pi)
    new_lon = original_location.lon + (dLon * 180 / math.pi)
    if type(original_location) is LocationGlobal:
        target_location = LocationGlobal(new_lat, new_lon, original_location.alt)
    elif type(original_location) is LocationGlobalRelative:
        target_location = LocationGlobalRelative(new_lat, new_lon, original_location.alt)
    else:
        raise Exception("Invalid Location object passed")
    return target_location


def get_distance_metres(a_location1, a_location2):
    dlat = a_location2.lat - a_location1.lat
    dlong = a_location2.lon - a_location1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5



