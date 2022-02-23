from opcua import Client
import time


class OpcuaClient:

    def __init__(self):
        self.client = None
        self.data = [("[size=14]16.02.2022", "[size=14]10", "[size=14]50", "[size=14]3", "[size=14]4", "[size=14]36", "[size=14]12", "[size=14]#F"),
                     ("[size=14]17.02.2022", "[size=14]11", "[size=14]53", "[size=14]5", "[size=14]3", "[size=14]26", "[size=14]12", "[size=14]#F")
                     ]

    def create_client(self, url):
        self.client = Client(url=url)
        self.client.connect()

    def add_data(self):
        """ Appends data to the self.data attribute """
        self.data.append(("[size=14]16.02.2022", "[size=14]10", "[size=14]50", "[size=14]3", "[size=14]4", "[size=14]36", "[size=14]12", "[size=14]#F"))
        #self.data.append(tuple(self.read_data()))  # it's very probable that there will be need to adjust the data format

    def read_data(self, ns=4, i=6):
        """ reads data from client's node defined in the function and returns all the values as a list """
        node = self.client.get_node(f'ns={ns};i={i}')
        row = []
        for child in node.get_children(): # w jakiej kolejności są te dane? według indeksów i czy według kolejności jak w bloku danych?
            row.append(child.get_value())
        row = [f"[size=14]{value}" for value in row]
        print(row)
        return tuple(row)

    def send_data(self, value, ns=4, i=4):
        """ Sends data to specified ns and i """
        variable = self.client.get_node(f'ns={ns};i={i}')
        variable.set_value(value)

    def terminate_client(self):
        self.client.disconnect()
