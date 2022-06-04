import kivy
kivy.require('1.9.0')

from kivy.storage.jsonstore import JsonStore
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty,NumericProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from os.path import join
# import tensorflow as tf
import time
# from plyer.platforms.android import accelerometer

# Create a class for all screens in which you can include
# helpful methods specific to that screen
class AppScreen(Screen):
    # data_dir = App().user_data_dir
    # store = JsonStore(join(data_dir, 'storage.json'))
    #
    # def login(self):
    #     username = self.login_username.text
    #     password = self.login_password.text
    #     AppScreen.store.put('credentials', username=username, password=password)
    pass
class MainScreen(Screen):

    # def __init__(self):
    #     super().__init__()
        # self.model=tf.keras.models.load_model('test_model.h5')
    chkinstat=ObjectProperty()
    chkoutstat = ObjectProperty()
    notstat= ObjectProperty()
    rmstat = ObjectProperty()
    state = NumericProperty(1)

    def chkstat(self):
        self.chkoutstat.disabled=False
        self.notstat.disabled=False
        self.rmstat.disabled=False
        self.chkinstat.disabled=True
        start=time.time()
        seconds=5
        def prt(elap):
            self.txt.text = str(elap)
        while self.state==1:
            current_time = time.time()
            elapsed=current_time-start
            print(elapsed)
            prt(elapsed)
            if elapsed>=seconds:
                self.chkoutstat.disabled = True
                self.notstat.disabled = True
                self.rmstat.disabled = True
                self.chkinstat.disabled = False
                break

    def sensor_data(self):
        accelerometer.enable()
        A_val = accelerometer.acceleration[:3]
        return A_val
    def check_out(self):
        self.state=0
        return self.state

    def predict(self,input):
        model=tf.keras.models.load_model('saved_model/my_model')
        model.predict(input)


class SettingScreen(Screen):
    pass


class MoghimiApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        # sm.add_widget(AppScreen(name='welcome'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingScreen(name='settings'))
        return sm



sample_app = MoghimiApp()
sample_app.run()