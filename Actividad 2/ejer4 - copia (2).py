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
  "apiKey": "AIzaSyAOyrlBHH-MIv4cSfJ4Q-0P5eBujsojRKY",
  "authDomain": "semana-i-7c2e6.firebaseapp.com",
  "databaseURL": "https://semana-i-7c2e6-default-rtdb.firebaseio.com",
  "projectId": "semana-i-7c2e6",
  "storageBucket": "semana-i-7c2e6.appspot.com",
  "messagingSenderId": "935089298155",
  "appId": "1:935089298155:web:fb68831bfff0c261de3cae"
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