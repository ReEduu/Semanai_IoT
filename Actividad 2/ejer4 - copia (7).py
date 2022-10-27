import pyrebase
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
"apiKey": "AIzaSyDEcTnQHxm1X7LbhUYpbC8NKzY_Y4HuLc0",
"authDomain": "semana-i-esp32-a01732165.firebaseapp.com",
"databaseURL": "https://semana-i-esp32-a01732165-default-rtdb.firebaseio.com",
"projectId": "semana-i-esp32-a01732165",
"storageBucket": "semana-i-esp32-a01732165.appspot.com",
"messagingSenderId": "119186266925",
"appId": "1:119186266925:web:82137a2fc4f071f80691a4"
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
