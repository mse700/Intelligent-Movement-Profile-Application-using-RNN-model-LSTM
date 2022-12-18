# Intelligent-Movement-Profile-Application

## Problem Statement

The Project is stemed from a case study with a list of requirements to be fullfilled. It is aimed to develope a mobile application being capable of recording the human activity based on accelerometer sensor. 


A Recurrent Neural Network model needs to be trained in order classify the input data (from Accelerometersensor) in to Sitting-Running-Sitting classes. The target framework can be either Android or IOS based on the user customization.

## Porject Requirements

Following requirements need to be met:
- The development Language must be Python
- Application Graphical Framework > Kivy, Kivy MD
- The settings must contain  personal data: name, age/ birth date, weight, height, job position, movement profile. The user needs to add them by first login.
- As the app user has to add personal data, only he/she should be able to read and write them. So, at app start, the user must unlock the access to his/her data. This is done by using FaceID, Touch ID or a simple passcode.
- The stored settings must be encrypted by using RSA or Fernet and are just readable by the application.
- The motivational task manager should use an own database (table) to select motivation tasks according to job type, gender, age and the actual movement profile. The database can be a separate file, which is read by the application.


<p align="center">
  <img width="1000" height="900" src="SW%20Flowchart.jpg">
</p>


## Project Structure

- The ``main.py`` contains main code for the application where all classes needed to trigger the app is available. The documentation provided for the code (line by line) is conveniently straight forward and easy to follow. 
- ``App.kv`` contains the graphical interface details in Kivy. For more information about kv files refer [here](https://kivy.org/doc/stable/)
- ``motivation.db`` contains motivational sentences proposed based on movement profile. This SQLite database file is queried by the app based on current movement profile.
- ``Query.py`` is a module containig query functions which provide data for the app.
- ``setting.py`` and ``setting.json`` is a setting menu template which is used by app to provide the setting menu, after first login, the user may enter the personal data.
- ``buildozer.spec`` is the generated specification file which bundles the app meta data in apk or ios frameework. It is recommended to install buildozer in order to handle the app generation task. More information about buildozer can be found [here](https://buildozer.readthedocs.io/en/latest/).
- ``Final_Model_liteV01.tflite`` is the trained LSTM model at the heart of the app, used for movement profile prediction.
- ``Time_Module.py`` contains time functions needed for reports.

## How to run/customize the App

Install the required packages (More instructions can be found [here](https://buildozer.readthedocs.io/en/latest/installation.html))

```console
pip install -r requirements.txt
```
Install the buildozer 

```console
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --user --upgrade Cython==0.29.19 virtualenv  # the --user should be removed if you do this in a venv

# add the following line at the end of your ~/.bashrc file
export PATH=$PATH:~/.local/bin/
```

After installation, initialize the buildozer to get a ```builozer.spec``` file. (However, the spec file is provided in the repo and can be editted)

```console
buildozer init
```

Following settings must be modified in spec file:

```console
source.include_exts = py,png,jpg,kv,atlas,tflite,db,xls,db,ext,json
requirements = python3,kivy,tensorflow,sqlite3,numpy,plyer,pandas,scikit-learn,datetime,xlrd,kivymd,cryptography,seaborn,xlrd,setuptools,rsa,scipy
requirements.source.kivy = ../../kivy
```

There is ```android specific``` and ```ios specific``` in the ```buildozer.spec```, where one can set the required settings.(The provided spec file in the repo is set for android)







