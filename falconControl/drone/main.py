from droneControl import falcon
helpMenu = "Welcome to the Falcon Control Center(TUI)" \
           "Here are the supported commands:" \
           "arm: arm the drone safely" \
           "takeoff <x>: takeoff with given value(x) 5 is default" \
           "land: to land" \
           "forward/back/right/left <x>: move to the given direction given values" \
           "rot_right/rot_left <x>: rotate given degrees(x)"

inp = raw_input("Is this a simulation run?(Yes or ip)")
vehicle = falcon.droneConnect(inp)
while inp != "land":
    # get command from user
    inp = raw_input("Command:")
    command = inp.split()
    # print the help menn
    if inp == "drone -h":
        print(helpMenu)
    elif command[0] == "arm":
        falcon.arm(vehicle)
    elif command[0] == "takeoff":
        if len(command) == 2:
            try:
                falcon.takeoff(vehicle, int(command[1]))
            except ValueError:
                print("ERROR: please enter a valid altidute for takeoff")
        else:
            falcon.takeoffDefault(vehicle)
    elif command[0] == "land":
        falcon.land(vehicle)
    elif (len(command) == 2) and (command[0] == "forward" or command[0] == "back" or command[0] == "right" or command[0] == "left"):
        try:
            falcon.move(vehicle, command[0], int(command[1]))
        except ValueError:
            print("ERROR: please enter a valid value for movement")
    elif (len(command) == 2) and (command[0] == "rot_right" or command[0] == "rot_left"):
        try:
            falcon.rotate(vehicle, command[0], int(command[1]))
        except ValueError:
            print("ERROR: please enter a valid value for rotation")

