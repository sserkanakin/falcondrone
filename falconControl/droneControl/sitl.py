from dronekit_sitl import SITL

# sitl.download("[copter", "3.3", verbose=False) # ...or download system (e.g. "copter") and version (e.g. "3.3")
# sitl.launch(["dronekit-sitl copter"], verbose=False, await_ready=False, restart=False)
# sitl.block_until_ready(verbose=False) # explicitly wait until receiving commands
# print (sitl.connection_string())
# code = sitl.complete(verbose=False) # wait until exit
# sitl.poll() # returns None or return code
# sitl.stop() # terminates SITL