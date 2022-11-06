import falcon
import paramiko
import time


def main():
    open('/usr/local/lib/python2.7/dist-packages/falcondrone/falconControl/drone/test.txt', 'w').close()
    open('/usr/local/lib/python2.7/dist-packages/falcondrone/falconControl/drone/commands.txt', 'w').close()
    client = ssh_client_connect()
    print("connected to ssh serkan")
    commands(client)


def run(line):
    f = open('/usr/local/lib/python2.7/dist-packages/falcondrone/falconControl/drone/test.txt', 'a')
    f.write(line)
    f.close()


def commands(client):
    land = True  # continue reading lines until drone lands
    connected = False  # check whether the connection is done
    with open('/usr/local/lib/python2.7/dist-packages/falcondrone/falconControl/drone/commands.txt',
              'r+') as fi:  # open file to write and read
        while land:  # while we have not received the land command which will end the program
            time.sleep(1)
            #if connected:
                #info = "echo " + vehicle.airspeed + " " + vehicle.location.global_relative_frame.alt + " " + vehicle.battery.level +  ">> /Users/serkanakin/Desktop/test.txt"
                #client.exec_command(info)
            if not connected:
                inf = 'echo "test passed">> /Users/serkanakin/Desktop/test.txt'
                client.exec_command(inf)
            line = fi.readline()  # read from commands.txt
            if line:  # when new command received
                print(line)
                if not connected:
                    if line != "s\n":  # actual connection over tcp
                        vehicle = falcon.droneConnect(line, 57600)
                    else:  # testing
                        print(line)
                        fi.write(line)
                        vehicle = "test"
                        connected = True
                elif vehicle == "test":
                    print(line)
                    if "land" in line:
                        land = False
                    fi.write(line)
                else:
                    land = readCommands(line, vehicle)


def readCommands(line, vehicle):
    command = line.split(':')  # split the command according to DroneL
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

def ssh_client_connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('172.20.10.2', username='serkanakin', password='082003')
    return client


main()
