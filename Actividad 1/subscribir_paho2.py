import paho.mqtt.client as paho
import statistics as stats
import numpy as np


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    if "frec" in msg.topic:
        frec = (str(msg.payload))
        frec = float(frec.split("'")[1])
        if(len(frecuencias)<6):
            frecuencias.append(frec) 
            #print(frec)
        else:
            print("Promedio Frecuencia: ",stats.mean(frecuencias))
            print("Maxima Frecuencia: ",max(frecuencias))
            print("Minima Frecuencia: ",min(frecuencias))
            print("\n")   
            frecuencias.clear()

    elif "nuc" in msg.topic:
        nucleo = (str(msg.payload))
        nucleo = float(nucleo.split("'")[1])
        if(len(nucleos)<7):
            nucleos.append(nucleo) 
           # print(nucleo)
        else:
            print("Promedio: de nucleos ",stats.mean(nucleos))
            print("Maximo numero de nucleos: ",max(nucleos))
            print("Minimo numero de nucleos: ",min(nucleos))
            print("\n")   
            nucleos.clear()


    elif "uso" in msg.topic:
        uso = (str(msg.payload))
        uso = float(uso.split("'")[1])
        if(len(usos)<6):
            usos.append(uso) 
            #print(uso)
        else:
            print("Promedio de uso: ",stats.mean(usos))
            print("Porcentaje de uso maximo: ",max(usos))
            print("Porcentaje de uso minimo: ",min(usos))
            print("\n")   
            usos.clear()

    elif "mem" in msg.topic:
        mem = (str(msg.payload))
        mem = float(mem.split("'")[1])
        if(len(memorias)<6):
            memorias.append(mem) 
            #print(mem)
        else:
            print("Promedio de porcentaje de memoria : ",stats.mean(memorias))
            print("Maximo porcentaje de memoria : ",max(memorias))
            print("Minimo porcentaje de memoria : ",min(memorias))
            print("\n")   
            memorias.clear()
    
    elif "proc" in msg.topic:    
        proc = (str(msg.payload))
        proc = proc.split("'")[1]
        if(len(procesos)<7):
            procesos.append(proc) 
            #print(mem)
        else:
            print("Lista de procesos más usados : ", procesos)
            print("\n")

            print("\n")   
            procesos.clear()


frecuencias = []
usos = []
nucleos = []
memorias = []
procesos = []
client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
#client.username_pw_set("etorresr", "G4t0")
client.connect("broker.mqttdashboard.com", 1883)
client.subscribe("dafne/frec", qos=1)
client.subscribe("miles/frec", qos=1)
#client.subscribe("dafne_badillo/frec", qos=1)
client.subscribe("victor/frec", qos=1)
client.subscribe("joseduardo/frec", qos=1)
client.subscribe("alonso/frec", qos=1)
client.subscribe("anthony/frec", qos=1)
client.subscribe("dafne/nuc", qos=1)
client.subscribe("dafne/uso", qos=1)
client.subscribe("dafne/mem", qos=1)
client.subscribe("dafne/proc", qos=1)
client.subscribe("miles/nuc", qos=1)
client.subscribe("miles/uso", qos=1)
client.subscribe("miles/mem", qos=1)
client.subscribe("miles/proc", qos=1)
client.subscribe("dafne_badillo/nuc", qos=1)
#client.subscribe("dafne_badillo/uso", qos=1)
#client.subscribe("dafne_badillo/mem", qos=1)
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
#client.subscribe("anthony/proc", qos=1)


client.loop_forever()
