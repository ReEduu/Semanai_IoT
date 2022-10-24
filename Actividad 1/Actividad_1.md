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
    ```
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
