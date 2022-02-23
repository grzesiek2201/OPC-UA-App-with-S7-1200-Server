from pandas import DataFrame, read_csv


def extract_data(data, columns=None):
    temp_rows = [[element.split(']')[1] for element in item] for item in data]
    df = DataFrame(temp_rows)
    if columns:
        df.columns = columns
    # df.columns = ['Date', 'Velocity [m/s]', 'Frequecny [Hz]', 'Amperage [A]', 'Torque [Nm]', 'Temperature [C]']
    df.to_csv('opcua_data.csv')


def import_data(path):
    df = read_csv(path, index_col=False)
    list_of_rows = [row[1:] for row in df.values]

    data = df.values.tolist()
    data = [row[1:] for row in data]
    data = [[str(value) for value in row] for row in data]

    return data
