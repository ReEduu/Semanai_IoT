# Actividad 2

En esta actividad se realizó una base de datos para almacenar los datos que generados en la actividad pasada, para ello se hizo uso de Firebase, ya que entre otras caracteristicas, tiene modalidad gratuita y ofrece base de datos no relacional en tiempo real, lo cual simplifica su uso. 

Asimismo se desarrollo un programa en Python capaz de enviar esta información a una base de datos en Firebase, en este sentido, se tuvieron que crear 8 programas con diferentes config para enviar la información a cada uno de los integrantes del salón.

A continuación se detalla el proceso llevado a cabo

- **Firebase**

  Se utilizó la base de datos creada en Firebase el dia de ayer. Los pasos seguidos fueron
  
  1. Iniciar sesión con cuenta de Google
  2. Crear nuevo proyecto
  3. Seleccionar Realtime Database
  4. Crear base de datos
  5. Para tener una API Key se tuvo que añadir un método de autenticación, en este caso anonimo
  
  A partir de este punto se empezó en la actividad del dia. Para la actividad se tuvo que
  
  1. Crear una nueva app web para generar los datos de config, necesarios para realizar la conexión desde Python
  2. Añadir un nuevo método de autenticación, aunque en este caso por correo electronico 
  3. En la sección de la base de datos, modificar las reglas de write y read a True
  
  Ya con estas acciones, la base de datos está lista para escribir y leer datos desde Python
  
- **Python**
 
  De lado de Python, fue necesario realizar la aplicación que envia datos de la computadora a las bases de los demás compañeros. A continuación se explica el código de uno de esos programas 
  
  Las librerias principales fueron pyrebase para realizar la conexión con la base de datos de Firebase, y psutil para obtener la información de la PC. Tambien se utilizo time para realizar el sleep de 2 minutos
  
     ``` Python
     import pyrebase
     import time
     import psutil
     ```
  El programa sólo tiene una función y es la misma que se utilizó en la actividad pasada. Devuelve una lista de procesos, ordenados del que consume más memoria al que consume menos
  
     ``` Python
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
