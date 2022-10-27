import pyrebase
import paho.mqtt.client as paho
from random import randint
import time
import psutil

def getListOfProcessSortedByMemory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           # Append dict to list
           listOfProcObjects.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
    return listOfProcObjects

config = {
  "apiKey" : "AIzaSyD57f8TRtQUYN76L04l-e7QYyVSmROWiNI",
  "authDomain" : "esp32-anthony.firebaseapp.com",
  "databaseURL" : "https://esp32-anthony-default-rtdb.firebaseio.com",
  "projectId" : "esp32-anthony",
  "storageBucket" : "esp32-anthony.appspot.com",
  "messagingSenderId" : "1031989251866",
  "appId" : "1:1031989251866:web:80ebc1ffeeefb86f1ba6a3"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
listOfRunningProcess = getListOfProcessSortedByMemory()
#create your onKey, for label elements
#update elements
while True:
    db.child("users").child("Eduardo").push({"frec":str(psutil.cpu_freq()[0]),"num":str(psutil.cpu_count()),"uso":str( psutil.cpu_percent(4)),"mem":str(psutil.virtual_memory()[2]),"proc":str(listOfRunningProcess[0]["name"])})
    #accesing database in firebase
    db = firebase.database()
    #reading some atributes of the onKey elements
    print("Datos añadidos")
    time.sleep(120)
