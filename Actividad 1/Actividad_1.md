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
  ```
  import paho.mqtt.client as paho
  from random import randint
  import time
  import psutil
  ```

