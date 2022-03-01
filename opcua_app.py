#:kivy: 2.0.0
from kivy.clock import Clock

import data_handling
import opcua_actions
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.button import *
from kivymd.uix.snackbar import Snackbar
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.popup import PopupException
# from android.permissions import request_permissions, Permission
# request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

# from matplotlib import pyplot as plt
# from kivy.garden.matplotlib import FigureCanvasKivyAgg

Window.size = (730, 600)

opc_client = opcua_actions.OpcuaClient()


class ConnectScreen(MDScreen):
    """ Class inheriting from MDScreen class, it's the Connect Screen """
    connected_string = StringProperty("Disconnected")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # always initialize the super class
        self.connected = False

    def on_connect(self):
        """ Action taken after the 'Connect' is button pressed"""
        # take text from the url field
        url = self.ids.connect_text_field.text
        print(f"{url = }")
        # either connect or disconnect, show Snackbar if exception
        try:
            if self.connected:
                opc_client.terminate_client()
            else:
                opc_client.create_client(url=url)
        except Exception as e:
            Snackbar(text="Couldn't connect, check the url", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
            print(e)
        else:
            self.connected = not self.connected
            if self.connected:
                self.connected_string = "Connected"
            else:
                self.connected_string = "Disconnected"
            Snackbar(text=f"{self.connected_string}", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()


class DataScreen(MDScreen):
    """ Class inheriting from MDScreen class, it's the Data Screen """
    # configure a popup
    file_chooser_popup = Popup(auto_dismiss=True,
                               size_hint=(0.8, 0.8),
                               pos_hint={'x': 0.1, 'top': 0.9},
                               title='Choose a file to open')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # always initialize the super class

        # initialize layouts and widgets
        self.file_box = MDBoxLayout(orientation='vertical')
        self.file_chooser = FileChooserListView()#(on_submit=self.load_data)
        self.button_box = MDBoxLayout(orientation='horizontal', size_hint=(0.8, 0.1), spacing=dp(20))

        # define columns headers
        self.cols = [("[size=14][anchor=right]Time", dp(20)),
                     ("[size=14][anchor=right]Vel [m/s]", dp(17)),
                     ("[size=14][anchor=right]Freq [Hz]", dp(17)),
                     ("[size=14][anchor=right]Amp [A]", dp(17)),
                     ("[size=14][anchor=right]Torq [Nm]", dp(17)),
                     ("[size=14][anchor=right]Temp [C]", dp(17)),
                     ("[size=14][anchor=right]Energy [J?]", dp(17)),
                     ("[size=14][anchor=right]ActualFault", dp(17))]
        self.rows = [("[size=14]16.02.2022", "[size=14]10", "[size=14]50", "[size=14]3", "[size=14]4", "[size=14]36", "[size=14]12", "[size=14]#F"),
                     ("[size=14]17.02.2022", "[size=14]9", "[size=14]40", "[size=14]3.5", "[size=14]3", "[size=14]26", "[size=14]12", "[size=14]#F"),
                     ("[size=14]17.02.2022", "[size=14]9", "[size=14]40", "[size=14]3.5", "[size=14]3", "[size=14]26", "[size=14]12", "[size=14]#F"),
                     ]
        self.table = None
        # schedule a initialize_screen method to execute once after the initialization
        Clock.schedule_once(self.initialize_screen)

    def open_popup(self):
        """ Open filechooser popup """
        self.file_chooser_popup.open()

    def close_popup(self, widget=None, path=None, object=None):
        """ Close filechooser popup """
        self.file_chooser_popup.dismiss()

    def initialize_screen(self, dt):
        """ Configure the screen """
        self.file_chooser_popup.add_widget(self.file_box)
        self.file_box.add_widget(self.file_chooser)
        self.file_box.add_widget(self.button_box)
        self.button_box.add_widget(MDFillRoundFlatButton(text="Open", on_release=self.load_data))
        self.button_box.add_widget(MDFillRoundFlatButton(text="Close", on_release=self.close_popup))
        self.add_table()

    def add_table(self):
        """ Add a table based on arguments' values """
        self.table = MDDataTable(
            size_hint=(1, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            check=False,
            use_pagination=True,
            rows_num=10,
            pagination_menu_height='240dp',
            column_data=self.cols,
            row_data=self.rows,
        )
        self.ids.table_box.add_widget(self.table)

    def update_table_from_server(self, widget):
        """ Update arguments' values based on data from the server """
        try:
            self.rows.insert(0, opc_client.read_data(ns=4, i=5))#? (tu trzeba gDB_toApp)
            # opc_client.add_data()
            # remove the widget
            self.ids.table_box.remove_widget(self.table)
            # update the data
            self.table = MDDataTable(
                size_hint=(1, 0.9),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                check=False,
                use_pagination=True,
                rows_num=10,
                pagination_menu_height='240dp',
                column_data=self.cols,
                row_data=self.rows #opc_client.data
            )
            # add the widget again
            self.ids.table_box.add_widget(self.table)
        except AttributeError as e:
            print(e)
            Snackbar(text="Couldn't download data", snackbar_x='10dp', snackbar_y='10dp',
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
        except IndexError as e:
            print(e)
            Snackbar(text="Couldn't download data", snackbar_x='10dp', snackbar_y='10dp',
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
        except ReferenceError as e:
            print(e)
            Snackbar(text="Couldn't download data", snackbar_x='10dp', snackbar_y='10dp',
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
        else:
            Snackbar(text="Data downloaded", snackbar_x='10dp', snackbar_y='10dp',
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()

    def export_data(self, widget):
        """ Export data to a .csv file named 'opcua_data.csv' """
        columns = ['Date', 'Velocity [m/s]', 'Frequecny [Hz]', 'Amperage [A]', 'Torque [Nm]', 'Temperature [C]', 'Energy [J]', 'ActualFault']
        try:
            data_handling.extract_data(opc_client.data)
        except PermissionError as e:
            print (e)
            Snackbar(text="Permission denied, try closing the 'opcua_data.csv' file", snackbar_x='10dp', snackbar_y='10dp',
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
        else:
            Snackbar(text="Data save under 'opcua_data.csv' file", snackbar_x='10dp', snackbar_y='10dp',
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()

    def load_data(self, widget):
        """ Export data to a .csv file named 'opcua_data.csv' """
        filename = self.file_chooser.selection
        print(filename)
        self.close_popup()
        try:
            self.rows = data_handling.import_data(filename[0])
        except Exception as e:
            print(e)
            Snackbar(text="Couldn't load data from file", snackbar_x='10dp', snackbar_y='10dp',
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
        else:
            self.ids.table_box.remove_widget(self.table)
            self.add_table()


class ControlScreen(MDScreen):
    """ Class inheriting from MDScreen class, it's the Control Screen """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # always initialize the super class

    def motor_start(self):
        try:
            opc_client.send_data(value=True, ns=4, i=3)
            print("motor start")
        except AttributeError as e:
            print(e)
            Snackbar(text="Couldn't send the command", snackbar_x='10dp', snackbar_y='10dp',
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()

    def motor_stop(self):
        try:
            opc_client.send_data(value=False, ns=4, i=3)
            print("motor stop")
        except AttributeError as e:
            print(e)
            Snackbar(text="Couldn't send the command", snackbar_x='10dp', snackbar_y='10dp',
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()

    def slider_change(self, touch):
        speed = self.ids.speed_slider.value
        # scale the speed value to required resolution, it's in 0-100% currently
        try:
            opc_client.send_data(value=float(speed), ns=4, i=4)
        except AttributeError as e:
            print(e)
            Snackbar(text="Couldn't send the command", snackbar_x='10dp', snackbar_y='10dp',
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
        print(self.ids.speed_slider.value)

    def error_acknowledge(self):
        print("error acknowledge")


class StatisticsScreen(MDScreen):
    """ Class inheriting from MDScreen class, it's the Statistics Screen """
    pass


class AboutScreen(MDScreen):
    """ Class inheriting from MDScreen class, it's the About Screen """
    pass


class ContentNavigationDrawer(MDBoxLayout):
    """ Class inheriting from MDBoxLayout class, it's the contents of the Navigation Drawer """
    pass


class OpcuaApp(MDApp):
    """ Class inheriting from MDApp class, it's the Main Application """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # always initialize the super class
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.accent_hue = "50"

    def build(self):
        return

    def on_stop(self):
        """ When application closes """
        try:
            opc_client.terminate_client()
            print("client terminated")
        except AttributeError:
            pass


def run_app():
    OpcuaApp().run()
