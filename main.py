''''

Moving Profile Application

'''

'''Importing the required Libraries'''
#import kivy
#kivy.require('1.9.1')
from kivy.config import Config
# Config.set('kivy','keyboard_mode','systemanddock')
from kivymd.app import MDApp
import sqlite3
from datetime import datetime, timedelta
from kivy.storage.jsonstore import JsonStore
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty,NumericProperty
from MovementSimulator import MPSimulator
from kivy.core.window import Window
from kivy.uix.popup import Popup
# from os.path import join
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
import time
from Query import data_query,pred,pred2
from plyer import accelerometer
from plyer import notification
import numpy as np
from tensorflow import lite
import random
from Time_Module import *
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import StringProperty
import matplotlib.pyplot as plt
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.settings import SettingsWithSidebar
from setting import settings_json
from kivy.config import Config
from kivy.storage.jsonstore import JsonStore
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import ast


class FirstScreen(Screen):
    '''The class providing the interface for welcome screen, the design of the page is added to the kv file and the
       corresponding methods are addressed here.'''
    def __init__(self, **kwargs):
        '''Initializing the class for reading the encrypted password from
            pass.ext located in the root folder'''
        super(Screen, self).__init__(**kwargs)
        with open('pass.ext','rb') as f:
            password=f.read() # reading the encrypted data from file
        private_key = self.get_private_key() # getting the private key
        original_message = private_key.decrypt(password,padding.OAEP(padding.MGF1(hashes.SHA256()),hashes.SHA256(), None)) # decrypting the password
        self.password = original_message.decode()  #password is added as an instance attribute

    def check_password(self):
        '''This method checks the entered password with the password read from encrypted file. if the password is right
            then it asks for sensor access otherwise Wrong Password will appear in the screen.if the access is approved by
            checking the box then it goes to the main screen '''
        if self.ids.passw.text==self.password: # password check
            self.ids.sensor_authorization.text='The Application needs access to your smart phone Accelerometer sensor.\n would you grant access to the sensor? (if Yes please check the box) '
            self.ids.enter.disabled=True #Disabling the Enter Button after successful password
            self.ids.checkbox.disabled=False #The checkbox is enabled
        else:
            self.ids.pass_message.text="Wrong Password" #message indicating wrong password

    def get_private_key (self):
        '''The (RSI) private key for decrypting the pass.ext is saved in the private_key.pem
            This method reads the private key
            Returns: Private Key'''
        with open("private_key.pem", "rb") as key_file:    #openning the file
            private_key = serialization.load_pem_private_key(key_file.read(),password=None,
                                                             backend=default_backend())
        return private_key

    def checkbox(self,instance,value):
        """
        This method controls the check box click, if the check box is clicked after correct password, then main screen
        will be opened
        """
        if value:
            self.manager.current='main' #Go to main screen

class MainScreen(Screen):
    '''Main Screen containing User Interface (UI) for dashboards as well as control buttons.
        The screen is designed in kv file and the supporting methods are provided under
        this class'''
    def spinner_clicked(self,value):
        '''The method monitors plan status for remind me button if the user changes
            the Excercise Plan, then the remind me button will be informed accordingly.'''
        self.plan=value

    def remind_me(self):
        '''This Method manages the correct hint when user presses Remind me button'''
        if self.ids.spinner_id.text=='Excercise Plan':
            '''if user press remind me button without chossing the prefered plan
                then a message will appear in the hint box to choose the plan first'''
            self.ids.hint.text = '\nHint:\nFirst, Select a Plan by hitting the Excercise Plan Button'
        else:
            '''There are 4 pre-defined plans for user to choose:
                1- 60 Min Daily Walk: it send a query to the database to get the walking duration during the current day, then
                    if the user did not achieve the goal the remaining walking minutes will appear in the hint box.
                    
                2- 30 Min Daily Walk: it send a query to the database to get the running duration during the current day, then
                    if the user did not achieve the goal the remaining running minutes will appear in the hint box.
                    
                3- 4 Hours Weekly Walk: it send a query to the database to get the walking duration during the current week, then
                    if the user did not achieve the goal, the remaining walking minutes will appear in the hint box.
                    
                4- 1 Hour Weekly Run: it send a query to the database to get the running duration during the current day, then
                    if the user did not achieve the goal, the remaining walking minutes will appear in the hint box.'''
            if self.plan=='60 Min Daily Walk':
                if daily_query()['Walking']>=60:    #Check the Walking minutes in the day
                    self.ids.hint.text='Great Job, You have achieved your Plan'
                else:
                    self.ids.hint.text=f'\nHint:\nYou need to walk {60-daily_query()["Walking"]} minutes more to achieve your Daily Walk plan'
            if self.plan=='30 Min Daily Run':
                if daily_query()['Running']>=30:
                    self.ids.hint.text='Great Job, You have achieved your Plan'
                else:
                    self.ids.hint.text=f'\nHint:\nYou need to run {30-daily_query()["Running"]} minutes more to achieve your Daily Run plan'
            if self.plan == '4 Hours Weekly Walk':
                if weekly_activity_query()['Walking'] >= 240:
                    self.ids.hint.text = 'Great Job, You have achieved your Plan'
                else:
                    self.ids.hint.text = f'\nHint:\nYou need to walk {240 - weekly_activity_query()["Walking"]} minutes more to achieve your Weekly Run plan'
            if self.plan == '1 Hours Weekly Run':
                if weekly_activity_query()['Running'] >= 60:
                    self.ids.hint.text = 'Great Job, You have achieved your Plan'
                else:
                    self.ids.hint.text = f'\nHint:\nYou need to run {60 - weekly_activity_query()["Running"]} minutes more to achieve your Weekly Run plan'

    def daily_results(self):
        '''This Method provides the daily plot to be indicated in the dashboard when Daily Report button is pressed.
            The plot contains 3 columns indicating the duration of each movement profile in the day'''
        self.ids.mat.clear_widgets()
        fix, ax = plt.subplots()
        ax.bar(daily_query().keys(), daily_query().values(),width=0.5) #Query the daily durations for activities
        plt.ylabel('Minutes')
        plt.grid(which='both', linestyle='--')
        plt.grid(which='minor', alpha=0.15)
        plt.title(f'{datetime.today().date().day}-{datetime.today().date().month}-{datetime.today().date().year}')
        self.box=self.ids.mat
        self.box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def weekly_results(self):
        '''This Method provides the weekly plot to be indicated in the dashboard when Weekly Report button is pressed.
            The figure indicates the movement profiles for each week days. In this regard, the data is saved based on
            the number of calendar week in the year'''
        self.ids.mat.clear_widgets()
        plt.clf()
        N = 7
        ind = np.arange(N)
        width = 0.15
        sit,walk,run=[],[],[]
        # print(datetime.today().isocalendar().week)
        for day in weekly_query().keys(): #Query the movement profile durations in current week
            sit.append(weekly_query()[day][0])
            walk.append(weekly_query()[day][1])
            run.append(weekly_query()[day][2])
        '''Plotting'''
        plt.bar(ind,sit,label='Sitting',width=0.15)
        plt.bar(ind+width,walk, label='Walking',width=0.15)
        plt.bar(ind+width*2,run, label='Running',width=0.15)
        plt.xticks(ind+width,['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
        plt.ylabel('Minutes')
        plt.grid(which='both', linestyle='--')
        plt.grid(which='minor', alpha=0.15)
        plt.title(f'Calender Week {datetime.today().isocalendar()[1]}')
        plt.legend()
        self.box1 = self.ids.mat
        self.box1.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def monthly_results(self):
        '''This Method provides the monthly plot to be indicated in the dashboard when Monthly Report is pressed.
            The figure indicates the movement profiles for each week days. In this regard, the data is saved based on
            months in the year'''
        plt.clf()
        self.ids.mat.clear_widgets()
        N = 12
        ind = np.arange(N)
        width = 0.15
        sit,walk,run=[],[],[]
        for month in monthly_query().keys():
            sit.append(monthly_query()[month][0])
            walk.append(monthly_query()[month][1])
            run.append(monthly_query()[month][2])
        plt.bar(ind,sit,label='Sitting',width=0.15)
        plt.bar(ind+width,walk, label='Walking',width=0.15)
        plt.bar(ind+width*2,run, label='Running',width=0.15)
        plt.xticks(ind+width,['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
        plt.ylabel('Minutes')
        plt.grid(which='both', linestyle='--')
        plt.grid(which='minor', alpha=0.15)
        plt.title(f'{datetime.today().isocalendar()[0]}')
        plt.legend()
        # plt.show()
        self.box2 = self.ids.mat
        self.box2.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def submit(self,mp):
        """
        This method adds the current movement profile, Date, Weekday, Calendar Week to the database
        """
        conn=sqlite3.connect('test_db.db') #Connect to the existing one
        c=conn.cursor() #Creat Cursor
        month=month_of_year(datetime.today().month) #Calculating the month
        weekday=day_of_week(datetime.today().weekday()) #Calculating the week
        c.execute(f"INSERT INTO appdata (Date,Month,Weekday,Week,Value) VALUES ('{datetime.today().date().year}-{datetime.today().date().month}-{datetime.today().date().day}','{month}','{weekday}','{datetime.today().isocalendar()[1]}','{mp}')")
        conn.commit()
        conn.close()

    

    def data_query(self):
        """
        This method makes a query to the smartphone accelerometer to read X,Y,Z
        :return: Movement Profile (Sitting,Walking,Running)
        """
        def get_acceleration():
            """
            This method reads the X,Y,Z of the smartphone accelerometer
            :return: (X,Y,Z)
            """
            val = accelerometer.acceleration[:3]
            return val
        x, y, z = [], [], []
        '''As the sample rate for the trained model is 13 so data reading will continue until the 13 values for
          X,Y,Z are provided'''
        while len(x) != 13:
            temp = get_acceleration()
            x.append(temp[0])
            y.append(temp[1])
            z.append(temp[2])
            time.sleep(0.05) #The time gap between each loop in order to get 13 values.
        data_list = [np.array(x), np.array(y), np.array(z)] #Change the list to numpy array
        self.data = np.transpose(data_list, (1, 2, 0)) #Transpose the data to be readable by model
        self.mp=self.pred(self.data) #Movement Profile Prediction
        return self.mp

    def mp_update(self):
        """
        This method updates the Movement Profile Box in the dashboard
        """
        self.ids.test_label.text=self.mp

    def pred(self,data_test):
        """
        This Method accepts the reshaped dataset and predict the movement profile using the tflite model.
        :param data_test: The dataset which the movement profile must be predicted accordingly
        :return: Movement Profile (Sitting,Walking,Running)
        """
        self.model.allocate_tensors()

        # Get input and output tensors.
        input_details = self.model.get_input_details()
        output_details = self.model.get_output_details()
        self.model.set_tensor(input_details[0]['index'], np.expand_dims(data_test[0], axis=0))
        self.model.invoke()
        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        output_data = self.model.get_tensor(output_details[0]['index'])
        #Returning the index of most probable prediction
        arg = np.argmax(output_data)
        if arg == 0:
            MP = 'Running'
        if arg == 1:
            MP = 'Sitting'
        if arg == 2:
            MP = 'Walking'
        return MP

    def check_in(self):
        """
        When Check In button in the dashboard is pressed, this method activates the movement profile prediction
         using tflite model
        """
        self.model = lite.Interpreter(model_path ='Final_Model_liteV01.tflite') #Load the tflite model
        '''In order to test the application functionality on PC a MP Simulator is created to simulate the sensor
            data reading. The Data is generated using the offline data gathered in the csv file'''
        data_test=MPSimulator()
        self.mp=self.pred(data_test) #Predicting the movement profile
        print(self.mp)
        '''When Deploying on the Smartphone, this line can be uncommented, this line runs the data query function to 
            read the current X,Y,Z from the smart phone accelerometer and predicts the movement profile'''
        # Clock.schedule_interval(self.data_query(), 1)
        '''Adding the Movement Profile every minute to database'''
        self.add_database=Clock.schedule_interval(lambda dt: self.submit(self.mp), 60)
        '''Updating the Movement Profile Box in the Dashboard'''
        self.update_dashboard=Clock.schedule_interval(lambda dt: self.mp_update(), 1)
        self.ids.checkout.disabled=False #Turn on Check out button
        self.ids.checkin.disabled=True #Turn off Check In button

    def check_out(self):
        """
        This method stops predicting the movement profile and adding it to database, this is triggered when check out
        button is pressed
        """
        self.add_database.cancel() #Cancel adding to database
        self.update_dashboard.cancel() #Cancel the dashboard update for movement profile
        self.ids.checkout.disabled = True #Turn off Check out Button
        self.ids.checkin.disabled = False #Turn on Check In button

class WindowManager(ScreenManager):
    '''This class manages the 3 Screens of App : FirstScreen - MainScreen'''
    pass

class App(MDApp):
    '''
    The main class which build the app based on moghimi.kv file in the root. Database connection, Notification Management,
    motivation task management and setting page are developed in this class.
    '''

    def build(self):
        """
        This is the main build method which loads the application based on the kv file
        :return: kv file app
        """
        kv = Builder.load_file('moghimi.kv') #Loading the kv file
        self.use_kivy_settings=False #Disable the kivy setting for the app
        # Choosing the Background Theme
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="BlueGray"
        '''The default age for handling the motivation task manager, user can enter the setting and change this value'''
        self.age=25
        '''The default gender for handling the motivation task manager, user can enter the setting and change this 
            value'''
        self.gender='Male'
        '''The default Notification rate for handling the motivation task manager, user can enter the setting and change
            this value'''
        self.notification_rate=7200
        '''Notification Interval'''
        self.notify_motivation=Clock.schedule_interval(lambda dt: self.motivation_task_manager(), self.notification_rate)
        self.connect_database() #Connecting to the Database
        return kv

    def connect_database(self):
        """
        Connection to SQLite database with its specifications(Columns)
        """
        conn=sqlite3.connect('test_db.db')
        c=conn.cursor()
        c.execute("""CREATE TABLE if not exists appdata(ID INTEGER PRIMARY KEY,Date date,Month text,Weekday text,Week int,Value text)""")
        conn.commit()
        conn.close()

    def start_stop_notification(self):
        """
        This method controls the start/stop notification when Pause Notification button in pressed.
        """
        if self.notify_motivation.is_triggered==1: #If notification is on this turns it off (Pause Notification)
            self.notify_motivation.cancel()
            self.show_notification('Notification Disabled')
        else: #If notification is off this turns it on (Resume Notification)
            self.notify_motivation = Clock.schedule_interval(lambda dt: self.motivation_task_manager(), int(self.notification_rate))
            self.show_notification('Notification Enabled')

    def show_notification(self,text):
        """
        This method accepts the text and pop up the notification in the smart phone
        :param text: The text to be shoen in the notification
        """
        notification.notify(title='Moghimi App', message=text,app_name="Moghimi App")

    def get_current_mp(self):
        """
        This method gets the current movement profile based on the last record in the database
        :return: The current movement profile
        """
        conn = sqlite3.connect('test_db.db') #Connecting to Database
        c = conn.cursor() # Creat Cursor
        c.execute(f"SELECT Value FROM appdata ORDER BY ID DESC LIMIT 1") #Query the last Record in Database
        record = c.fetchall()
        return record[0][0]

    def mp_query(self,profile,frame):
        """
        This method makes a query of the moving profile based on timeframe as well as activity profile
        :param profile: The activity profile (Sitting, Walking, Running)
        :param frame: The time frame which the activity is queried (Daily,Weekly,Monthly)
        :return: The sume of activity profile in time frame in minutes
        """
        conn = sqlite3.connect('test_db.db')#Connect to Database
        c = conn.cursor() # Creat Cursor
        '''Daily Query'''
        if frame=='Daily':
            c.execute(f"SELECT COUNT(Value) AS dailystate1 FROM appdata WHERE Value='{profile}' AND Date='{datetime.today().date().year}-{datetime.today().date().month}-{datetime.today().date().day}'")
            record = c.fetchall()
        '''Weekly Query'''
        if frame=='Weekly':
            d = datetime.today() - timedelta(days=7) # Calculating the date of last week (today - 7 day)
            from_date = d.date()
            c.execute(
                f"SELECT COUNT(Value) AS weeklystate1 FROM appdata WHERE Value='{profile}' AND Date BETWEEN '{from_date.year}-{from_date.month}-{from_date.day}' AND '{datetime.today().date().year}-{datetime.today().date().month}-{datetime.today().date().day}'")
            record = c.fetchall()
        '''Monthly Query'''
        if frame=='Monthly':
            d = datetime.today() - timedelta(days=30) ## Calculating the date of last month (today - 30 day)
            from_date2 = d.date()
            c.execute(
                f"SELECT COUNT(Value) AS monthlystate1 FROM appdata WHERE Value='{profile}' AND Date BETWEEN '{from_date2.year}-{from_date2.month}-{from_date2.day}' AND '{datetime.today().date().year}-{datetime.today().date().month}-{datetime.today().date().day}'")
            record = c.fetchall()
        return record[0][0]

    def two_hours_mp_notification(self):
        '''
        Getting the Movement Profile Summary for last 2 hours From Database in a Dictionary
        { 'Sitting':x,'Walking':y,'Running':z}

        return: The appropriate notification based on movement profile in the last 2 hours
        '''
        activity_history={}
        conn = sqlite3.connect('test_db.db') #Connect to Database
        c = conn.cursor()
        for activity in ['Sitting','Walking','Running']:#Query the the movement profile for the last 120 Minutes
            c.execute(f"select COUNT(Value) from (select * from appdata order by ID desc limit 120) Where Value= '{activity}'")
            act = c.fetchall()
            activity_history[activity]=act[0][0]
        if activity_history['Sitting']>120: #If sitting more than 120 Minutes
            self.show_notification('Do not sit any more, Walk even slow!!')
        if activity_history['Walking'] > 120: #If walking more than 120 Minutes
            self.show_notification('Stop and sit for a some time and chill out!!')
        if activity_history['Running'] > 120: #If running more than 120 Minutes
            self.show_notification('Wow, 2 Hours Run is a big deal, Try to slow down to walk speed!!')

    def motivation_task_manager(self):
        """
        This method controls the motivational task manager.
        return: Appropriate Notification based on Gender, Age and Daily/Weekly/Monthly Movement Profile
        """
        gender=self.gender #The Gender which is entered in app setting
        age=self.age #The age which is entered in the app setting

        '''two_hours_mp_notification provides appropriate notification if the user is in a movement profile in the last 
            two hours.'''
        self.two_hours_mp_notification()

        '''current_mp_notification provides appropriate notification baased on current movement profile'''
        self.current_mp_notification()
        conn = sqlite3.connect('motivation.db') #Connect to Database

        '''Managing Notification for Weekly Movement Profile (Pushed based on the duration of Walking per Week)'''
        '''Weekly Motivational Notification is set on four days in 4 weeks of the month. In every months 4th,11th,18th and 25th 
            are in 4 different weeks of the month.'''
        if datetime.today().date().day in (4,11,18,25):
            walk_weekly = self.mp_query('Walking', 'Weekly') #Query the movement profile
            if gender == 'Male':
                if walk_weekly < 140: #The notifications are queried based on gender as well as age range
                    if 20 < age <= 40:
                        c = conn.cursor()
                        #Query the messages from database for young men who do not walk more than 140 Minutes in week
                        c.execute(f"SELECT message FROM motivation WHERE Weekly=1 AND Age=1 AND Gender=1")
                        record = c.fetchall()
                        self.show_notification(record[0][0])

                    if 41 < age <= 55:
                        c = conn.cursor()
                        #Query the messages from database for middle-age men who do not walk more than 140 Minutes in week
                        c.execute(f"SELECT message FROM motivation WHERE Weekly=1 AND Age=2 AND Gender=1")
                        record = c.fetchall()
                        self.show_notification(record[0][0])

                    if age > 55:
                        c = conn.cursor()
                        #Query the messages from database for old men who do not walk more than 140 Minutes in week
                        c.execute(f"SELECT message FROM motivation WHERE Weekly=1 AND Age=3 AND Gender=1")
                        record = c.fetchall()
                        self.show_notification(record[0][0])
            elif gender == 'Female':
                if walk_weekly < 120: #The notifications are queried based on gender as well as age range
                    if 20 < age <= 40:
                        c = conn.cursor()
                        #Query the messages from database for young women who do not walk more than 120 Minutes in week
                        c.execute(f"SELECT message FROM motivation WHERE Weekly=1 AND Age=1 AND Gender=2")
                        record = c.fetchall()
                        self.show_notification(record[0][0])

                    if 41 < age <= 55:
                        c = conn.cursor()
                        #Query the messages from database for middle-age women who do not walk more than 120 Minutes in week
                        c.execute(f"SELECT message FROM motivation WHERE Weekly=1 AND Age=2 AND Gender=2")
                        record = c.fetchall()
                        self.show_notification(record[0][0])

                    if age > 55:
                        c = conn.cursor()
                        #Query the messages from database for old women who do not walk more than 120 Minutes in week
                        c.execute(f"SELECT message FROM motivation WHERE Weekly=1 AND Age=3 AND Gender=2")
                        record = c.fetchall()
                        self.show_notification(record[0][0]) #The notifications are queried based on gender as well as age range

        '''Managing Notification for Monthly Movement Profile (Pushed based on the duration of Walking per Month)'''
        '''Monthly Motivational Notification is set on 30th of each month.'''
        if datetime.today().date().day==30:
            walk_monthly = self.mp_query('Walking', 'Monthly')
            if gender == 'Male':
                if walk_monthly < 300: #The notifications are queried based on gender as well as age range
                    if 20 < age <= 40:
                        c = conn.cursor()
                        #Query the messages from database for young men who do not walk more than 300 Minutes in month
                        c.execute(f"SELECT message FROM motivation WHERE Monthly=1 AND Age=1 AND Gender=1")
                        record = c.fetchall()
                        self.show_notification(record[0][0])

                    if 41 < age <= 55:
                        c = conn.cursor()
                        #Query the messages from database for middle-age men who do not walk more than 300 Minutes in month
                        c.execute(f"SELECT message FROM motivation WHERE Monthly=1 AND Age=2 AND Gender=1")
                        record = c.fetchall()
                        self.show_notification(record[0][0])

                    if age > 55:
                        c = conn.cursor()
                        #Query the messages from database for old men who do not walk more than 300 Minutes in month
                        c.execute(f"SELECT message FROM motivation WHERE Monthly=1 AND Age=3 AND Gender=1")
                        record = c.fetchall()
                        self.show_notification(record[0][0])

            elif gender == 'Female':
                if walk_monthly < 280: #The notifications are queried based on gender as well as age range
                    if 20 < age <= 40:
                        c = conn.cursor()
                        # Query the messages from database for young women who do not walk more than 280 Minutes in month
                        c.execute(f"SELECT message FROM motivation WHERE Monthly=1 AND Age=1 AND Gender=2")
                        record = c.fetchall()
                        self.show_notification(record[0][0])

                    if 41 < age <= 55:
                        c = conn.cursor()
                        # Query the messages from database for middle-age women who do not walk more than 280 Minutes in month
                        c.execute(f"SELECT message FROM motivation WHERE Monthly=1 AND Age=2 AND Gender=2")
                        record = c.fetchall()
                        self.show_notification(record[0][0])

                    if age > 55:
                        c = conn.cursor()
                        # Query the messages from database for old women who do not walk more than 280 Minutes in month
                        c.execute(f"SELECT message FROM motivation WHERE Monthly=1 AND Age=3 AND Gender=2")
                        record = c.fetchall()
                        self.show_notification(record[0][0])

        '''Managing Notification for Daily Movement Profile (Pushed based on the duration of Running)'''
        '''Daily Motivational Notification is set for running at least 2 minutes a day'''
        run_daily = self.mp_query('Running', 'Daily') #Query the Daily Running from Database
        if run_daily<2:
            self.show_notification('Try to run at least for 2 Minutes')

    def build_config(self, config):
        """
        This method provides a tool for making a setting page for app based on key-value dictionary.
        A json file created for providing an example of what setting items look like, after the first login in the application,
        the user is able to enter individual data, the information will be stored in app configuration until adjusted
        again by user.
        """
        config.setdefaults('example',
                           {"Name": JsonStore('setting.json').get("Name"),
                            "Gender": JsonStore('setting.json').get("Gender"),
                            "Age": JsonStore('setting.json').get("Age"),
                            "Birthday": JsonStore('setting.json').get("Birthday"),
                            "Height": JsonStore('setting.json').get("Height"),
                            "Weight": JsonStore('setting.json').get("Weight"),
                            "Job Position": JsonStore('setting.json').get("Job Position"),
                            "Notification": JsonStore('setting.json').get("Notification"),
                            "Language": JsonStore('setting.json').get("Language")})

    def build_settings(self, settings):
        """
        The setting template is made in a setting.py file.
        This file is just a template for setting items and does not contain any confidential data.
        """
        settings.add_json_panel('Setting',self.config,data=settings_json) #add setting.py as setting template

    def on_config_change(self, config, section, key, value):
        """
        This method controls if any setting default item be changed. In case of any change, the corresponding variable
        in the application will be changed.

        for example:
        the default age in the application is 25, when user changes the age to 32 then the application motivational
        task manager will know that the user is 32 years old.

        """
        # if the age is changed, the age in the app will be changed with the new age
        if key=='Age':
            self.age=int(value)
        # if notification rate is changed, the notification rate in the app will be changed with the new notification rate
        if key == 'Notification':
            self.notification_rate=int(value)*3600
        # if user Gender is changed, the Gender in the app will be changed with the new Gender
        if key == 'Gender':
            self.gender=str(value)

    def current_mp_notification(self):
        """
        This method provides appropriate notification based on current movement profile
        """
        conn = sqlite3.connect('motivation.db') # Connect to Database
        age=self.age
        self.mp=self.get_current_mp() # Get the current movement profile
        if self.mp=='Sitting': # Providing one of the appropriate messages based on age in the database when Sitting
            if 20 < age <= 40:
                c = conn.cursor()
                c.execute(f"SELECT message FROM motivation WHERE Sitting=1 AND Age=1")
                record = c.fetchall()
                c = conn.cursor()
                c.execute(f"SELECT message FROM motivation WHERE Sitting=1 AND Age=0")
                records = c.fetchall()
                lst = [item[0] for item in records]
                lst.append(record[0][0])
                self.show_notification(random.choice(lst))

            if 41 < age <= 55:
                c = conn.cursor()
                c.execute(f"SELECT message FROM motivation WHERE Sitting=1 AND Age=1")
                record = c.fetchall()
                c = conn.cursor()
                c.execute(f"SELECT message FROM motivation WHERE Sitting=1 AND Age=1")
                records = c.fetchall()
                lst = [item[0] for item in records]
                lst.append(record[0][0])
                self.show_notification(random.choice(lst))

            if age > 55:
                c = conn.cursor()
                c.execute(f"SELECT message FROM motivation WHERE Sitting=1 AND Age=1")
                record = c.fetchall()
                c = conn.cursor()
                c.execute(f"SELECT message FROM motivation WHERE Sitting=1 AND Age=2")
                records = c.fetchall()
                lst = [item[0] for item in records]
                lst.append(record[0][0])
                self.show_notification(random.choice(lst))

        if self.mp=='Walking': # Providing one of the appropriate messages based on age in the database when Walking
            c = conn.cursor()
            c.execute(f"SELECT message FROM motivation WHERE Walking=1")
            record = c.fetchall()
            lst = [item[0] for item in record]
            self.show_notification(random.choice(lst))

        if self.mp=='Running': # Providing one of the appropriate messages based on age in the database when Running
            c = conn.cursor()
            c.execute(f"SELECT message FROM motivation WHERE Running=1")
            record = c.fetchall()
            lst = [item[0] for item in record]
            self.show_notification(random.choice(lst))



''' Run the Application'''
App().run()

