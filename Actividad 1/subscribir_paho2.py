import paho.mqtt.client as paho
import statistics as stats
import numpy as np


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    if "frec" in msg.topic:
        frec = (str(msg.payload))
        frec = float(frec.split("'")[1])
        if(len(frecuencias)<5):
            frecuencias.append(frec) 
            print(frec)
        else:
            print(stats.mean(frecuencias))   
            frecuencias.clear()

    elif "nuc" in msg.topic:
        nucleo = (str(msg.payload))
        nucleo = float(nucleo.split("'")[1])
        if(len(nucleos)<7):
            nucleos.append(nucleo) 
            print(nucleo)
        else:
            print(stats.mean(nucleos))   
            nucleos.clear()


    elif "uso" in msg.topic:
        uso = (str(msg.payload))
        uso = float(uso.split("'")[1])
        if(len(usos)<7):
            usos.append(uso) 
            print(uso)
        else:
            print(stats.mean(usos))   
            usos.clear()

    elif "mem" in msg.topic:
        mem = (str(msg.payload))
        mem = float(mem.split("'")[1])
        if(len(memorias)<7):
            memorias.append(mem) 
            print(mem)
        else:
            print(stats.mean(memorias))   
            memorias.clear()
    
    else:    
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))


frecuencias = []
usos = []
nucleos = []
memorias = []
client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
#client.username_pw_set("etorresr", "G4t0")
client.connect("broker.mqttdashboard.com", 1883)
client.subscribe("dafne/frec", qos=1)
client.subscribe("miles/frec", qos=1)
#client.subscribe("dafne_badillo/frec", qos=1)
#client.subscribe("victor/frec", qos=1)
client.subscribe("joseduardo/frec", qos=1)
client.subscribe("alonso/frec", qos=1)
client.subscribe("anthony/frec", qos=1)
"""
client.subscribe("dafne/nuc", qos=1)
client.subscribe("dafne/uso", qos=1)
client.subscribe("dafne/mem", qos=1)
client.subscribe("dafne/proc", qos=1)
client.subscribe("miles/nuc", qos=1)
client.subscribe("miles/uso", qos=1)
client.subscribe("miles/mem", qos=1)
client.subscribe("miles/proc", qos=1)
client.subscribe("dafne_badillo/nuc", qos=1)
client.subscribe("dafne_badillo/uso", qos=1)
client.subscribe("dafne_badillo/mem", qos=1)
client.subscribe("dafne_badillo/proc", qos=1)
client.subscribe("victor/nuc", qos=1)
client.subscribe("victor/uso", qos=1)
client.subscribe("victor/mem", qos=1)
client.subscribe("victor/proc", qos=1)
client.subscribe("joseduardo/nuc", qos=1)
client.subscribe("joseduardo/uso", qos=1)
client.subscribe("joseduardo/mem", qos=1)
client.subscribe("joseduardo/proc", qos=1)
client.subscribe("alonso/nuc", qos=1)
client.subscribe("alonso/uso", qos=1)
client.subscribe("alonso/mem", qos=1)
client.subscribe("alonso/proc", qos=1)
client.subscribe("anthony/nuc", qos=1)
client.subscribe("anthony/uso", qos=1)
client.subscribe("anthony/mem", qos=1)
client.subscribe("anthony/proc", qos=1)
"""


client.loop_forever()
