import paho.mqtt.client as paho
from random import randint
import time
import psutil

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

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

client = paho.Client()
#client.username_pw_set("etorresr", "G4t0")
client.on_publish = on_publish
client.connect("broker.mqttdashboard.com", 1883)
client.loop_start()

while True:
    temperature = randint(1,30)
    listOfRunningProcess = getListOfProcessSortedByMemory()
    (rc, mid) = client.publish("joseduardo/test",
    str(temperature), qos=1)
    (rc, mid) = client.publish("joseduardo/frec",
    str(psutil.cpu_freq()[0]), qos=1)
    (rc, mid) = client.publish("joseduardo/uso",
    str( psutil.cpu_percent(4)), qos=1)
    (rc, mid) = client.publish("joseduardo/nuc",
    str(psutil.cpu_count()), qos=1)
    (rc, mid) = client.publish("joseduardo/mem",
    str(psutil.virtual_memory()[2]), qos=1)
    (rc, mid) = client.publish("joseduardo/proc",
    str(listOfRunningProcess[0]["name"]), qos=1)
    print(temperature)
    print('The CPU usage is: ', psutil.cpu_percent(4))
    print("Number of cores in system", psutil.cpu_count())
    print("CPU Statistics", psutil.cpu_stats())
    print("CPU frequency", psutil.cpu_freq())
    print("CPU load average 1, 5, 15 minutes", psutil.getloadavg())
    print(psutil.virtual_memory())
    print(psutil.sensors_battery()) 
    time.sleep(30)
