from datetime import datetime, timedelta
import sqlite3
def day_of_week(day):
    """

    :param day: The number of week day from 0:Monday to 6:Sunday
    :return: The corresponding Day in string
    """
    if day==0:
        return 'Monday'
    if day==1:
        return 'Tuesday'
    if day==2:
        return 'Wednesday'
    if day==3:
        return 'Thursday'
    if day==4:
        return 'Friday'
    if day==5:
        return 'Saturday'
    if day==6:
        return 'Sunday'

def month_of_year(month):
    """

    :param month: The month number
    :return: The corresponding Month in string
    """
    if month==1:
        return 'January'
    if month==2:
        return 'February'
    if month==3:
        return 'March'
    if month==4:
        return 'April'
    if month==5:
        return 'May'
    if month==6:
        return 'June'
    if month==7:
        return 'July'
    if month==8:
        return 'August'
    if month==9:
        return 'September'
    if month==10:
        return 'October'
    if month==11:
        return 'November'
    if month==12:
        return 'December'

def daily_query():
    '''This Function makes a query in the database and provides a dictionary containing the Activities as keys and
        corresponding minutes as value

        Return : dict{'Sitting':x,'Walking':y,'Running':z}'''

    conn = sqlite3.connect('test_db.db') #Connect to the Database
    daily={}
    c = conn.cursor() # Creat Cursor
    '''Daily Update : Query the daily durations'''
    c.execute(
        f"SELECT COUNT(Value) AS dailystate FROM appdata WHERE Value='Running' AND Date='{datetime.today().date().year}-{datetime.today().date().month}-{datetime.today().date().day}'")
    record = c.fetchall()
    daily['Running']=record[0][0]
    c.execute(
        f"SELECT COUNT(Value) AS dailystate FROM appdata WHERE Value='Walking' AND Date='{datetime.today().date().year}-{datetime.today().date().month}-{datetime.today().date().day}'")
    record1 = c.fetchall()
    daily['Walking'] = record1[0][0]
    c.execute(
        f"SELECT COUNT(Value) AS dailystate FROM appdata WHERE Value='Sitting' AND Date='{datetime.today().date().year}-{datetime.today().date().month}-{datetime.today().date().day}'")
    record2 = c.fetchall()
    daily['Sitting'] = record2[0][0]
    return daily

def weekly_query():
    '''This Function makes a weekly query in the database and provides a dictionary containing the Weekdays as keys
        and corresponding minutes as values

        Returns : dict{'Monday':[Sitting(minutes),Walking(minutes),Running(minutes)],
                      'Tuesday':[Sitting(minutes),Walking(minutes),Running(minutes)],
                      'Wednesday':[Sitting(minutes),Walking(minutes),Running(minutes)],
                      'Thursday':[Sitting(minutes),Walking(minutes),Running(minutes)],
                      'Friday':[Sitting(minutes),Walking(minutes),Running(minutes)],
                      'Saturday':[Sitting(minutes),Walking(minutes),Running(minutes)],
                      'Sunday':[Sitting(minutes),Walking(minutes),Running(minutes)]}'''
    '''Weekly Update'''
    conn = sqlite3.connect('test_db.db') #Connect to Database
    weekly = {}
    c = conn.cursor() # Creat Cursor
    days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    activities=['Sitting','Walking','Running']
    for day in days:
        day_activity_list=[]
        for activity in activities:
            c.execute(
                f"SELECT COUNT(Value) AS weeklystate FROM appdata WHERE Value='{activity}' AND Weekday='{day}' AND Week='{datetime.today().isocalendar()[1]}'")
            record3 = c.fetchall()
            day_activity_list.append(record3[0][0])
        weekly[day]=day_activity_list
    return weekly

def weekly_activity_query():
    '''For Remind Me Button'''
    '''Weekly Update'''
    conn = sqlite3.connect('test_db.db')
    weekly_activity = {}
    # Creat Cursor
    c = conn.cursor()
    activities=['Sitting','Walking','Running']
    for activity in activities:
        c.execute(
            f"SELECT COUNT(Value) AS weeklystate FROM appdata WHERE Value='{activity}' AND Week='{datetime.today().isocalendar()[1]}'")
        record3 = c.fetchall()
        weekly_activity[activity] = record3[0][0]
    return weekly_activity

def monthly_query():
    '''This Function makes a monthly query in the database and provides a dictionary containing Months as keys and
        corresponding minutes as value

            Returns : dict{'January':[Sitting(minutes),Walking(minutes),Running(minutes)],
                          'February':[Sitting(minutes),Walking(minutes),Running(minutes)],
                          'March':[Sitting(minutes),Walking(minutes),Running(minutes)],
                          'April':[Sitting(minutes),Walking(minutes),Running(minutes)],
                          'May':[Sitting(minutes),Walking(minutes),Running(minutes)],
                          'June':[Sitting(minutes),Walking(minutes),Running(minutes)],
                          'July':[Sitting(minutes),Walking(minutes),Running(minutes)]
                          'August':[Sitting(minutes),Walking(minutes),Running(minutes)]
                          'Septempber':[Sitting(minutes),Walking(minutes),Running(minutes)]
                          'October':[Sitting(minutes),Walking(minutes),Running(minutes)]
                          'November':[Sitting(minutes),Walking(minutes),Running(minutes)]
                          'December':[Sitting(minutes),Walking(minutes),Running(minutes)]}'''
    '''Monthly Update'''
    conn = sqlite3.connect('test_db.db') #Connect to Database
    monthly = {}
    c = conn.cursor() # Creat Cursor
    months=['January','February','March','April','May','June','July','August','Septempber','October','November','December']
    activities=['Sitting','Walking','Running']
    for month in months:
        month_activity_list=[]
        for activity in activities:
            c.execute(
                f"SELECT COUNT(Value) AS weeklystate FROM appdata WHERE Value='{activity}' AND Month='{month}'")
            record4 = c.fetchall()
            month_activity_list.append(record4[0][0])
        monthly[month]=month_activity_list
    return monthly

