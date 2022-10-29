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

Para la base de datos se utilizó la misma creada en 

**Resultados**

Al finalizar la actividad se desarrolló un sistema capaz de mandar datos capturados por 3 distintos sensores desde el ESP32 hasta una base de datos en Firebase, así como de recibir dos datos de la misma base, con el fin de cambiar la intensidad de un LED y el digito de un display. Asimismo, desde una aplicación movil creada en App Inventor, se pudieron mostrar las mediciones realizadas y mandar los datos para cambiar la intensidad de un LED y el digito del Display.

El funcionamiento fue mostrado en clase y a continuación se muestra una imagen con el sistema realizado 

![Circuito completo](./20221026_172338.jpg)
