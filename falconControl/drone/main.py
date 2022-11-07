import falcon
import paramiko
import time


def main():
    open('/usr/local/lib/python2.7/dist-packages/falcondrone/falconControl/drone/test.txt', 'w').close()
    open('/usr/local/lib/python2.7/dist-packages/falcondrone/falconControl/drone/commands.txt', 'w').close()
    i = 0
    with open('/usr/local/lib/python2.7/dist-packages/falcondrone/falconControl/drone/commands.txt',
              'r') as fi:  # open file to write and read
            while i == 0:
                info = fi.readline()
                if info:
                    info = info.split(':')
                    client = ssh_client_connect(info)
                    i = 1
            while i == 1:
                target_file = fi.readline()
                if target_file:
                    i = 2
    run("connected to ssh serkan")
    commands(client, target_file)


def run(line):
    f = open('/usr/local/lib/python2.7/dist-packages/falcondrone/falconControl/drone/test.txt', 'a')
    f.write(line)
    f.close()


def commands(client, target_file):
    target_file = target_file.replace(" ", "\ ")
    land = True  # continue reading lines until drone lands
    connected = False  # check whether the connection is done
    time.sleep(5)
    open('/usr/local/lib/python2.7/dist-packages/falcondrone/falconControl/drone/test.txt', 'w').close()
    open('/usr/local/lib/python2.7/dist-packages/falcondrone/falconControl/drone/commands.txt', 'w').close()
    with open('/usr/local/lib/python2.7/dist-packages/falcondrone/falconControl/drone/commands.txt',
              'r+') as fi:  # open file to write and read
        while land:  # while we have not received the land command which will end the program
            time.sleep(1)
            if connected:
                info = "echo " + vehicle.airspeed + " " + vehicle.location.global_relative_frame.alt + " " + vehicle.battery.level + " >> " + target_file
                client.exec_command(info)
            if not connected:
                inf = 'echo "test passed" >> ' + target_file
                client.exec_command(inf)
                run("here\n")
            line = fi.readline()  # read from commands.txt
            if line:  # when new command received
                print(line)
                if not connected:
                    if line != "s\n":  # actual connection over tcp
                        vehicle = falcon.droneConnect(line, 57600)
                    else:  # testing
                        fi.write(line)
                        vehicle = "test"
                        connected = True
                elif vehicle == "test":
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

def ssh_client_connect(info):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(info[0], username = info[1], password = info[2][:-1])
    return client


main()
