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
  
  ``Python  
    import pyrebase
    import time
    import psutil
  ``
