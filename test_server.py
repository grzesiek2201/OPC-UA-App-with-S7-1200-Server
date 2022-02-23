from time import sleep
import random
from opcua import Server

server = Server()
server.set_endpoint("opc.tcp://127.0.0.1:12345")

server.register_namespace("PLC1")

objects = server.get_objects_node()
print(objects)

to_app = objects.add_object('ns=4;i=2', "gDB_toApp")  # ns=namespace, s=string
print(to_app)

current = to_app.add_variable('ns=4;i=9', "absoluteCurrent", 10)
fault = to_app.add_variable('ns=4;i=13', "actualFault", 1234)
freq = to_app.add_variable('ns=4;i=8', "actualFrequency", 50)
speed = to_app.add_variable('ns=4;i=7', "actualSpeed", 13)
energy = to_app.add_variable('ns=4;i=11', "energy", 2)
temp = to_app.add_variable('ns=4;i=10', "motorTemperature", 21)
word = to_app.add_variable('ns=4;i=6', "statusWord", 0)
torque = to_app.add_variable('ns=4;i=12', "torque",8)

# bulb = objects.add_object(2, "Light Bulb")  # this creates NumericNodeId instead of StringNodeId
# state = bulb.add_variable(2, "State of Light Bulb", False)
# print(state)
# state.set_writable()

# temperature = 20.0

try:
    print("Start Server")
    server.start()
    print("Server Online")
    while True:
        print(f"{current.get_value() = }\n{fault.get_value() = }\n{freq.get_value() = }\n{speed.get_value() = }\n"
              f"{energy.get_value() = }\n{temp.get_value() = }\n{word.get_value() = }\n{torque.get_value() = }\n")
        # temperature = random.uniform(19, 21)
        # temp.set_value(temperature)
        # print(f"New Temperature: {temp.get_value()}")
        # print(f"State of Light Bulb: {state.get_value()}")
        sleep(2)

finally:
    server.stop()
    print("Server Offline")
