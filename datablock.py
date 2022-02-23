class DataBlock:

    def __init__(self):
        self.data = []

    def add_value(self, value):
        self.data.append(value)

    def add_list(self, values):
        """ values are of type list """
        self.data.append(values)