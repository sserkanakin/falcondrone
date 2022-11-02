import falcon
import time

helpMenu = "Welcome to the Falcon Control Center(TUI)\n" \
           "Here are the supported commands:\n" \
           "arm: arm the drone safely\n" \
           "takeoff <x>: takeoff with given value(x) 5 is default\n" \
           "land: to land\n" \
           "forward/back/right/left <x>: move to the given direction given values\n" \
           "rot_right/rot_left <x>: rotate given degrees(x)\n"

def main():
    run("connect\n")
    commands()

def run(line):
    f = open('/home/drone/.local/lib/python2.7/site-packages/falconControl/drone/test.txt', 'a')
    f.write(line)
    f.close()

def commands():
    #inp = raw_input("Is this a simulation run?(Yes or ip)")
    # for now to skip the connection phase and test
    land = True
    count = 0
    connected = False
    with open('/home/drone/.local/lib/python2.7/site-packages/falconControl/drone/commands.txt', 'r+') as file:
        while land:
            count = count + 1
            line = file.readline()
            if line:
                if not connected  and line != "s\n":
                    #vehicle = falcon.droneConnect(line)
                    connected = False
                elif line == "s\n":
                    print(line)
                    vehicle = "test"
                    connected = True
                else:
                    command = line.split(':')
                    # print the help menu
                    if line == "drone -h":
                        print(helpMenu)
                    elif command[0] == "arm":
                        print("arm")
                        falcon.arm(vehicle)
                    elif command[0] == "toff":
                        run(line)
                        file.write("toff\n")
                        if len(command) == 2 and command[1] != "1":
                            try:
                                falcon.takeoff(vehicle, int(command[1]))
                            except ValueError:
                                print("ERROR: please enter a valid altidute for takeoff")
                        else:
                            falcon.takeoffDefault(vehicle)
                    elif command[0] == "land":
                        falcon.land(vehicle)
                        land = False
                    elif (len(command) == 2) and (
                            command[0] == "forward" or command[0] == "back" or command[0] == "right" or command[
                        0] == "left"):
                        try:
                            falcon.move(vehicle, command[0], int(command[1]))
                        except ValueError:
                            print("ERROR: please enter a valid value for movement")
                    elif (len(command) == 2) and (command[0] == "rot_right" or command[0] == "rot_left"):
                        try:
                            falcon.rotate(vehicle, command[0], int(command[1]))
                        except ValueError:
                            print("ERROR: please enter a valid value for rotation")

main()