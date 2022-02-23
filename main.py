from opcua import Client
import time
import opcua_app

# create client
# client = Client("opc.tcp://192.168.0.2:4840/freeopcua/server/")
# client.connect()

# get objects handle from client
# print(f"{client.get_namespace_array() = }")
# objects = client.get_objects_node()
# print(f"{objects = }")

# node_1 = objects.get_children()
# server_interfaces = node_1[2]
# server_interfaces = client.get_node('ns=3;s="ServerInterfaces"')
# server_interface_1 = server_interfaces.get_children()
# data_block = server_interface_1.get_children()[0]
# print(data_block.get_value())
# print(server_interfaces.get_children())


# while True:
#     values = client.get_node('ns=4;i=2')
#     for child in values.get_children():
#         print(child.get_value())    # print(values.get_children())
#     word_1 = client.get_node('ns=4;i=3')
#     print(word_1.get_value())
#     time.sleep(1)


# # get objects and their children from objects handle
# tempsens = objects.get_children()[1]
# bulb = objects.get_children()[2]
# print(f"{bulb.get_children() = }")
# print(f"{bulb.get_children()[0].get_browse_name() = }")
#
# state = bulb.get_children()[0]
# print(f"{state.get_value() = }")
#
# state.set_value(True)
# print(f"{state.get_value() = }")
#
# print(f"{tempsens.get_children() = }")
# for child in tempsens.get_children():
#     print(f"{child.get_value() = }")
#
# # another way to get node's children
# temp = client.get_node('ns=2;s="TS1_Temperature"')
# print(f"{temp.get_value() = }")

# client.close_session()

if __name__ == '__main__':
    opcua_app.run_app()
