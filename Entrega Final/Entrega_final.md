# Entrega Final

En el siguiente reporte se explican los detalles de la entrega final de la Semana I, esta consiste en un sistema con el ESP32, el cual realiza mediciones de tres variables fisicas para posteriormente mandar los datos a una base de datos en Firebase, asimismo toma los datos de dos variables en Firebase, para cambiar la señal de un PWM, y mandar un digito en un display de 7 segmentos. A partir de esta base de datos, una aplicación de app inventor tomarán los datos almacenados para mostrar las distintas mediciones, tambien podrá mandar datos diferentes para cambiar el valor del PWM y mostrar un digito diferente en el display

**Conexiones con el ESP32**

Para medir las variables fisicas se utilizarón los siguientes sensores:

- Sensor PIR de movimiento
- Sensor DHT11 de temperatura y humedad
- Sensor HC-SR04 de distancia 

Para este proyectto las variables fisicas a medir fueron:

- Movimiento (True o False)
- Humedad (Porcentaje de humedad)
- Distancia (en cm)

Tambien se utilizaron los siguientes componentes para mostrar el envio de datos desde la app y su posterior recibimiento en el ESP32

- Un LED que varia su intensidad según la señal PWM
- Un display 7 segmentos que varia su digito según el numero guardado en la base

En el siguiente diagrama se muestran las conexiones realizadas con el ESP32

![Diagrama de conexiones realizadas](./Semana_I.png)}

Tambien se enlistan los pines usados 

- D15-> Trig del sensor ultrasonico
- D2--> Echo del sensor ultrasonico
- D4 --> Segundo pin del sensor de humedad
- RX2 --> LED
- D5 --> b del display
- D18 --> a del display
- D19 --> c del display
- RX0 --> d del display
- TX0 --> e del display
- D22 --> g del display
- D23 --> f del display
- D12 --> pin de enmedio del sensor PIR

**Base de datos de Firebase**

Para la base de datos se utilizó la misma creada en la actividad pasada. Donde tenemos los siguientes valores almacenados:

- Digito (String)
- PWM (String)
- Distancia (Numero)
- Humedad (Numero)
- Movimiento (Booleano)

En el caso de digito y PWM, estos son cadenas, ya que App Inventor al mandar la información, automaticamente convierte los valores enteros en cadenas, esto se soluciona en el código de Arduino convirtiendo las cadenas en enteros 

Esta base de datos es a tiempo real, por lo que se actualiza cada vez que se recibe o cambia un valor, lo cual es util para mostrar el funcionamiento. Si se quiere ahondar un poco más, en el reporte de la actividad 2 se especifican los pasos a seguir para crearla

**App Inventor**

Se utilizó App Inventor para crear una aplicación que funcione como interfaz para el envio y recibo de la información recopilada en la base de datos. Se crearon las siguientes pantallas:

- Pantalla de Inicio
  
  Es la pantalla inicial, donde se puede seleccionar con dos botones, tanto mediciones como envio de datos
  
- Mediciones
  
  Aqui se muestra una imagen de los tres sensores junto con su respectiva información, la cual se actualiza cada vez que un dato cambia en la base de datos
  
- Envio de datos

  En la ultima pantalla se encuentra la imagen del LED y el display 7 segmentos, junto a una caja de texto donde introducir el valor a mandar. La información en las cajas de texto, se manda cada segundo gracias a que se añadio un timer como componente
  
Para realizar la conexión con la base de datos, se uso el componente de Firebase, incluido en App Inventor como función experimental

**Código de Arduino**

**Resultados**

Al finalizar la actividad se desarrolló un sistema capaz de mandar datos capturados por 3 distintos sensores desde el ESP32 hasta una base de datos en Firebase, así como de recibir dos datos de la misma base, con el fin de cambiar la intensidad de un LED y el digito de un display. Asimismo, desde una aplicación movil creada en App Inventor, se pudieron mostrar las mediciones realizadas y mandar los datos para cambiar la intensidad de un LED y el digito del Display.

El funcionamiento fue mostrado en clase y a continuación se muestra una imagen con el sistema del ESP32 realizado

![Circuito completo](./20221026_172338.jpg)
