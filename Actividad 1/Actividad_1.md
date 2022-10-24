# Actividad 1

La siguiente actividad consiste en realizar la suscripción y publicación de distintos tópicos en un broker, utilizando el lenguaje Python y usando el protocolo MQTT, para ello cada uno de los integrantes del grupo debía publicar los siguientes datos de sus computadoras personales:

-	Frecuencia del CPU
-	Numero de núcleos del CPU
-	 Porcentaje de uso de CPU
-	Porcentaje de memoria RAM disponible
-	Proceso que consume más recursos

Es importante mencionar que el Publisher manda una cadena de texto, y para facilitar el posterior trabajo de casteo, los tópicos con más de un parámetro como la frecuencia, memoria RAM, o procesos que consumen más recursos, sólo deben mandar la información requerida.

De lado del código del suscriptor, es donde está la mayor parte del trabajo, ya que una vez que recibe la cadena del bróker, este debe separar sólo el dato requerido, convertirlo a flotante, guardarlo en una lista, y calcular el mínimo, máximo y promedio, para posteriormente mandar a imprimir los datos. Esto aplica en casi todos los tópicos, con excepción de los procesos que consumen más recursos, donde simplemente se manda a imprimir la lista con los procesos que consumen más recursos de cada equipo  

**Código**

A continuación se explicará brevemente el código, el cual consiste en dos partes:

1. Publisher

   Se empizan importando las librerias requeridas, en este caso paho.mqtt funciona para realizar la conexión con el broker, mientras que psutil te ayuda a obtener la información requerida del equipo
     ``` Python
     import paho.mqtt.client as paho
     from random import randint
     import time
     import psutil
     ```
   
   Este programa cuenta con dos funciones  
   on_publis: se ejecuta cuando se publica un nuevo tópico y unicamente te dice el numero de publicación (mid)  
   getListOfProcessSortedByMemory: te devuelve los procesos ejecutados por el equipo, ordenados del que consume más recursos al que menos 
   ``` Python
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
    ```
    
   Se realiza la conexión con el broker, en este caso se hace uso del puerto 1883 que es libre  
    ``` Python
   client = paho.Client()
   client.on_publish = on_publish
   client.connect("broker.mqttdashboard.com", 1883)
   client.loop_start()
    ```
    
   El programa principal es un loop infinito que cada 30 segundos, publica la información de los topicos solicitados (frecuencia, uso de memoria, nucleos, etc) una vez publicada la información, se imprimen los mismos datos en la consola a manera de verificar que sean correctos
    ```Python
    while True:
    listOfRunningProcess = getListOfProcessSortedByMemory()
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
    ```

   
2. Subscriber


   En el caso del código del subscriber, este es el más trabajado, debido a que se necesitaban obtener los datos del broker y con ello calcular las metrícas solicitadas
   
   Empieza utilizando igual que en el código pasado, la libería paho.mqtt para realizar la conexión, en este caso use statics para calcular el promedio de una lista con una función
     ``` Python
     import paho.mqtt.client as paho
     import statistics as stats
     ```
   
   Este programa tambien cuenta con dos funciones  
   on_subscribe: se ejecuta cada vez que es suscrito a un nuevo topico, generalmente al inicio de la ejecución
   on_message: este es el proceso más importante. Se ejecuta cada que se recibe un nuevo dato de los tópicos suscritos. En este caso lo que hago es que dependiendo del tópico del dato, este realizará un proceso u otro, aunque en general es casi lo mismo, con excepción de cuando se recibe un proceso, ya que no se tienen que calcular la media, maximo y minimo, sólo guardarlo en una lista. El proceso a seguir es el siguiente: 
   - Verificamos el topico del dato
   - Convertimos el dato recibido a String
   - Separamos la información que necesitamos con split y convertimos a flotante
   - Si la longitud del arreglo es menor a 7 entonces añadimos el elemento a su lista correspondiente
   - En caso contrario imprimimos la frecuencia maxima, minima y promedio y limpiamos la lista
   - El proceso es el mismo con frecuencia, memoria, uso de CPU y nucleos
   ``` Python
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
                  procesos.clear()

    ```
   La parte final del código simplemente consiste en definir las listas, conectarse al broken y subscribirse a cada uno de los tópicos de los compañeros del grupo
    ``` Python
   frecuencias = []
   usos = []
   nucleos = []
   memorias = []
   procesos = []
   client = paho.Client()
   client.on_subscribe = on_subscribe
   client.on_message = on_message
   client.connect("broker.mqttdashboard.com", 1883)
   client.subscribe("dafne/frec", qos=1)
   client.subscribe("miles/frec", qos=1)
   client.subscribe("dafne_badillo/frec", qos=1)
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


   client.loop_forever()

    ```
    
**Resultados**

Al ejecutar el programa se obtuvo la siguiente tabla

|             | Minimo      |Maximo       | Promedio    |
| ----------- | ----------- |-----------  |-----------  |
| Frecuencia  | 1601        | 2808        | 2552.87     |
| Nucleos     | 2           | 8           | 2           |
| Uso         | 3           | 25.18       | 12.4        |
| Memoria     | 56.68       | 74.2        | 32.2        |

Lista de procesos: code, name, firefox.exe, msedge.exe, taskhostw.exe, code, name

Como se puede observar hay computadoras que tienen pocos nucleos, así como una baja frecuencia, sin embargo el promedio del uso del CPU es bastante bajo, mientras que el de la memoria es algo alto. Por ultimo en la lista de procesos, no hay ningun patrón en especifico, simplemente se repite visual studio code en dos ocasiones.  

Para finalizar se adjunta el link al video con el programa corriendo
https://www.youtube.com/watch?v=Aae3DDBW1TE
