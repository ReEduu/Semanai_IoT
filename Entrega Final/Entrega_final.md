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

A continuación se explica brevemente las partes del código de Arduino, cargado al ESP32

El código, realiza las siguientes tareas

- Realizar la conexión al WiFi del TEC, la cual se realiza al inicio del set up y para lo que se ocupa la libreria WiFi.h
- Realizar la conexión a Firebase, para ello se utiliza la libreria Firebase_ESP_Client.h y se realiza despues de la conexión a internet
- Realizar y mandar cada una de las mediciones

  - Humedad: hace uso de la ibreria DHT.h
  - Movimiento: realiza el proceso para realizar las mediciones según la configuración dada
  - Distancia: se realizan los calculos necesarios para obtener las mediciones en cm según los datos del sensor

  Cada una de estas variables, una vez medidas, se mandan continuamente a la base de datos con ayuda de la función Firebase.RTDB.set (float, boolean o string)
- Recuperar datos de la base de datos

``` C
#include "DHT.h"

#define DHTPIN 4     // Digital pin connected to the DHT sensor
// Feather HUZZAH ESP8266 note: use pins 3, 4, 5, 12, 13 or 14 --
// Pin 15 can work but DHT must be disconnected during program upload.

// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11
//#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

// Initialize DHT sensor.
// Note that older versions of this library took an optional third parameter to
// tweak the timings for faster processors.  This parameter is no longer needed
// as the current DHT reading algorithm adjusts itself to work on faster procs.
DHT dht(DHTPIN, DHTTYPE);

#include <esp_wpa2.h>
#include <Arduino.h>
#if defined(ESP32)
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
#endif
#include <Firebase_ESP_Client.h>

//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// Insert your network credentials
const char* ssid = "Tec"; 
#define EAP_IDENTITY "A01732165@tec.mx"
#define EAP_PASSWORD ""

// Insert Firebase project API Key
#define API_KEY "AIzaSyDEcTnQHxm1X7LbhUYpbC8NKzY_Y4HuLc0"

// Insert RTDB URLefine the RTDB URL */
#define DATABASE_URL "https://semana-i-esp32-a01732165-default-rtdb.firebaseio.com/" 

const int trigPin = 15;
const int echoPin = 2;
const int ledPin = 16; // 16 corresponds to GPIO16

// setting PWM properties
const int freq = 5000;
const int ledChannel = 0;
const int resolution = 8;

//define sound speed in cm/uS
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701


//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
bool movimiento = false;
bool signupOK = false;
String intValue = "0";
//bool boolValue;
String pwmValue;


const int PIN_TO_SENSOR = 12; // GIOP19 pin connected to OUTPUT pin of sensor
int pinStateCurrent   = LOW;  // current state of pin
int pinStatePrevious  = LOW;  // previous state of pin

long duration;
float distanceCm;
float distanceInch;

//se demuestra el manejo del display de siete segmentos

//se declaran los pines a usar
//int LEDs[] = {8,9,7,6,4,3,2};        // for Arduino microcontroller
//int LEDs[] = {D2,D1,D3,D4,D6,D7,D8}; // for ESP8266 microcontroller
int LEDs[] = {22,23,1,3,19,18,5};    // for ESP32 microcontroller


//se declaran los arreglos que forman los dígitos
int zero[] = {0, 1, 1, 1, 1, 1, 1};   // cero
int one[] = {0, 0, 0, 0, 1, 1, 0};   // uno
int two[] = {1, 0, 1, 1, 0, 1, 1};   // dos
int three[] = {1, 0, 0, 1, 1, 1, 1};   // tres
int four[] = {1, 1, 0, 0, 1, 1, 0};   // cuatro 
int five[] = {1, 1, 0, 1, 1, 0, 1};   // cinco
int six[] = {1, 1, 1, 1, 1, 0, 1};   // seis
int seven[] = {1, 0, 0, 0, 1, 1, 1};   // siete
int eight[] = {1, 1, 1, 1, 1, 1, 1}; // ocho
int nine[] = {1, 1, 0, 1, 1, 1, 1};   // nueve
int ten[] = {1, 1, 1, 0, 1, 1, 1};   // diez, A
int eleven[] = {1, 1, 1, 1, 1, 0, 0};   // once, b
int twelve[] = {0, 1, 1, 1, 0, 0, 1};   // doce, C
int thirteen[] = {1, 0, 1, 1, 1, 1, 0};   // trece, d
int fourteen[] = {1, 1, 1, 1, 0, 0, 1};   // catorce, E
int fifteen[] = {1, 1, 1, 0, 0, 0, 1};   // quince, F


//se declara contador
unsigned char contador = 0;

//función que despliega del 0 al F
void segment_display(unsigned char valor)
{
    switch(valor)
    {
        case 0:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], zero[i]);
                    break;
        case 1:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], one[i]);
                    break;
        case 2:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], two[i]);
                    break;
        case 3:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], three[i]);
                    break;
        case 4:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], four[i]);
                    break;
        case 5:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], five[i]);
                    break;
        case 6:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], six[i]);
                    break;
        case 7:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], seven[i]);
                    break;
        case 8:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], eight[i]);
                    break;
        case 9:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], nine[i]);
                    break;
        case 10:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], ten[i]);
                    break;
        case 11:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], eleven[i]);
                    break;
        case 12:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], twelve[i]);
                    break;
        case 13:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], thirteen[i]);
                    break;
        case 14:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], fourteen[i]);
                    break;
        case 15:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], fifteen[i]);
                    break; 
        default:
                    for (int i = 0; i<7; i++) digitalWrite(LEDs[i], zero[i]);
                    break;          
    }
}




void setup() 
{
  Serial.begin(115200);

  // WPA2 enterprise magic starts here
    WiFi.disconnect(true);      
    WiFi.mode(WIFI_STA);   //init wifi mode
    Serial.printf("Connecting to WiFi: %s ", ssid);
    //esp_wifi_sta_wpa2_ent_set_ca_cert((uint8_t *)incommon_ca, strlen(incommon_ca) + 1);
    esp_wifi_sta_wpa2_ent_set_identity((uint8_t *)EAP_IDENTITY, strlen(EAP_IDENTITY));
    esp_wifi_sta_wpa2_ent_set_username((uint8_t *)EAP_IDENTITY, strlen(EAP_IDENTITY));
    esp_wifi_sta_wpa2_ent_set_password((uint8_t *)EAP_PASSWORD, strlen(EAP_PASSWORD));
    //esp_wifi_sta_wpa2_ent_enable();
    esp_wpa2_config_t configW = WPA2_CONFIG_INIT_DEFAULT();
    esp_wifi_sta_wpa2_ent_enable(&configW);
    // WPA2 enterprise magic ends here
    WiFi.begin(ssid);
  
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(300);
    }
    Serial.println();
    Serial.print("Connected with IP: ");
    Serial.println(WiFi.localIP());
    Serial.println();

    /* Assign the api key (required) */
    config.api_key = API_KEY;

    /* Assign the RTDB URL (required) */
    config.database_url = DATABASE_URL;

    /* Sign up */
    if (Firebase.signUp(&config, &auth, "", ""))
    {
        Serial.println("ok");
        signupOK = true;
    }
    else
    {
        Serial.printf("%s\n", config.signer.signupError.message.c_str());
    }

    /* Assign the callback function for the long running token generation task */
    config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h
  
    Firebase.begin(&config, &auth);
    Firebase.reconnectWiFi(true);
  
  Serial.println(F("DHTxx test!"));
  for (int i = 0; i<7; i++) pinMode(LEDs[i], OUTPUT);

  dht.begin();
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(PIN_TO_SENSOR, INPUT); // set ESP32 pin to input mode to read value from OUTPUT pin of sensor
  ledcSetup(ledChannel, freq, resolution);
  ledcAttachPin(ledPin, ledChannel);
}

void loop() 
{
  // Wait a few seconds between measurements.
  delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) 
  {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.print(f);
  Serial.print(F("°F  Heat index: "));
  Serial.print(hic);
  Serial.print(F("°C "));
  Serial.print(hif);
  Serial.println(F("°F"));


  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
    
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate the distance
  distanceCm = duration * SOUND_SPEED/2;
  
  // Convert to inches
  distanceInch = distanceCm * CM_TO_INCH;
  
  // Prints the distance in the Serial Monitor
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);
  Serial.print("Distance (inch): ");
  Serial.println(distanceInch);

  pinStatePrevious = pinStateCurrent; // store old state
  pinStateCurrent = digitalRead(PIN_TO_SENSOR);   // read new state

  if (pinStatePrevious == LOW && pinStateCurrent == HIGH) 
  {   // pin state change: LOW -> HIGH
    movimiento = true;
    Serial.println("Motion detected!");
    // TODO: turn on alarm, light or activate a device ... here
  }
  else if (pinStatePrevious == HIGH && pinStateCurrent == LOW) 
  {   // pin state change: HIGH -> LOW
    movimiento = false;
    Serial.println("Motion stopped!");
    // TODO: turn off alarm, light or deactivate a device ... here
  }

  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 2000 || sendDataPrevMillis == 0))
    {
        sendDataPrevMillis = millis();
        
        // Write an Int number on the database path test/movimiento
        if (Firebase.RTDB.setBool(&fbdo, "test/movimiento", movimiento))
        {
            Serial.println("PASSED");
            Serial.println("PATH: " + fbdo.dataPath());
            Serial.println("TYPE: " + fbdo.dataType());
        }
        else 
        {
            Serial.println("FAILED");
            Serial.println("REASON: " + fbdo.errorReason());
        }
    
        // Write an Float number on the database path test/humedad
        if (Firebase.RTDB.setFloat(&fbdo, "test/humedad", h))
        {
            Serial.println("PASSED");
            Serial.println("PATH: " + fbdo.dataPath());
            Serial.println("TYPE: " + fbdo.dataType());
        }
        else 
        {
            Serial.println("FAILED");
            Serial.println("REASON: " + fbdo.errorReason());
        }

         // Write an Float number on the database path test/distancia
        if (Firebase.RTDB.setFloat(&fbdo, "test/distancia", distanceCm))
        {
            Serial.println("PASSED");
            Serial.println("PATH: " + fbdo.dataPath());
            Serial.println("TYPE: " + fbdo.dataType());
        }
        else 
        {
            Serial.println("FAILED");
            Serial.println("REASON: " + fbdo.errorReason());
        }
        
        //lee primer dato
        if (Firebase.RTDB.getString(&fbdo, "/test/digito")) 
        {
            if (fbdo.dataType() == "string") 
            {
                intValue = fbdo.stringData();
                Serial.println(intValue);
            }
        }
        else 
        {
            Serial.println(fbdo.errorReason());
        }
        //lee segundo dato
        if (Firebase.RTDB.getString(&fbdo, "/test/pwm")) 
        {
            if (fbdo.dataType() == "string") 
            {
                pwmValue = fbdo.stringData();
                Serial.println(pwmValue);
            }
        }
        else 
        {
            Serial.println(fbdo.errorReason());
        }
    }
  
  ledcWrite(ledChannel, pwmValue.toInt());
  segment_display(intValue.toInt());
  delay(1000);

}
```

**Resultados**

Al finalizar la actividad se desarrolló un sistema capaz de mandar datos capturados por 3 distintos sensores desde el ESP32 hasta una base de datos en Firebase, así como de recibir dos datos de la misma base, con el fin de cambiar la intensidad de un LED y el digito de un display. Asimismo, desde una aplicación movil creada en App Inventor, se pudieron mostrar las mediciones realizadas y mandar los datos para cambiar la intensidad de un LED y el digito del Display.

El funcionamiento fue mostrado en clase y a continuación se muestra una imagen con el sistema del ESP32 realizado

![Circuito completo](./20221026_172338.jpg)
