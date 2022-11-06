import falcon


def main():
    run("connect\n")
    commands()


def run(line):
    f = open('/home/drone/.local/lib/python2.7/site-packages/falconControl/drone/test.txt', 'a')
    f.write(line)
    f.close()


def commands():
    land = True  # continue reading lines until drone lands
    connected = False  # check whether the connection is done
    with open('/home/drone/.local/lib/python2.7/site-packages/falconControl/drone/commands.txt',
              'r+') as fi:  # open file to write and read
        while land:  # while we have not received the land command which will end the program
            line = fi.readline()  # read from commands.txt
            if line:  # when new command received
                if not connected:
                    if line != "s\n":  # actual connection over tcp
                        vehicle = falcon.droneConnect(line, 57600)
                    else:  # testing
                        print(line)
                        vehicle = "test"
                    connected = True
                else:
                    land = readCommands(line, vehicle)


def readCommands(line, vehicle):
    command = line.split(':')  # split the command according to protocol language
    if command[0] == "toff":
        falcon.takeoff(vehicle, command[1])
        return False
    elif command[0] == "land":
        falcon.land(vehicle)
        return True
    elif command[0] == "move":
        movement = command[1]
        if movement == "u":
            falcon.move_vertical(vehicle, int(command[2])/5 * -1, 5)
        elif movement == "d":
            falcon.move_vertical(vehicle, int(command[2])/5, 5)
        elif movement == "o":
            falcon.rotate(vehicle, command[2])
        else:
            falcon.move_horizontal(vehicle, movement, int(command[2]))
        return False
    elif command[0] == "sped":
        vehicle.airspeed = int(command[2])


main()
