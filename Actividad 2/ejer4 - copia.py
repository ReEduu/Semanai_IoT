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
  "apiKey": "AIzaSyC7RSVPwD1ZYsX_qQDUxWC_kGHofArUtWA",
  "authDomain": "semana-i-esp32-dafne.firebaseapp.com",
  "databaseURL": "https://semana-i-esp32-dafne-default-rtdb.firebaseio.com",
  "projectId": "semana-i-esp32-dafne",
  "storageBucket": "semana-i-esp32-dafne.appspot.com",
  "messagingSenderId": "270923728104",
  "appId": "1:270923728104:web:8525a5e22d28e1f7a7355d"


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