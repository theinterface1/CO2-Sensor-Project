/*
  Attempt at prgraming ESP8266 module with K-30 CO2 Sensor
*/

#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include <WiFiClientSecure.h>

#ifndef STASSID
#define STASSID "SensorCenter"
#define STAPSK  "SoxTiger"
#define IPAddr  "192.168.4.1"  //192.168.4.1

#endif

char* ssid = STASSID;
char* password = STAPSK;


//Set up a serial port for talking to the sensor
SoftwareSerial sensorSerial(0,2); //GPIO 0 for Rx and GPIO 2 for Tx

byte readCO2[] = {0xFE, 0X44, 0X00, 0X08, 0X02, 0X9F, 0X25}; //poll command on sensor
byte response[] = {0x01,0x02,0x03,0x04,0x05,0x06,0x07}; //array to store response
byte serverData[] = {0,0,0,0,0,0,0}; //array to store requests from the serever

int delayTime = 5000; //5000 milliseconds between polls

WiFiClient client;

void setup() 
{
  Serial.begin(9600);
  sensorSerial.begin(9600);
  Serial.println("ready");

  //Conect to wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);             // Connect to the network
  Serial.print("Connecting to ");
  Serial.print(ssid); Serial.println(" ...");

  int i = 0;
  while (WiFi.status() != WL_CONNECTED) { // Wait for the Wi-Fi to connect
    delay(1000);
    Serial.print(++i); Serial.print(' ');
  }

  Serial.println('\n');
  Serial.println("Connection established!");  
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());         // Send the IP address of the ESP8266 to the computer

  //Connect to server
  bool connection_successful = 0;
  while( !connection_successful )
  {
    connection_successful = client.connect(IPAddr, 10000);
    if (connection_successful) 
    {
      Serial.println("Success!");
      //let server know you're ready
      client.write(0xEE);
    }
    else
    {
      Serial.println("Failure");  
    }
  }
}

void loop() 
{
  awaitPoll();
  sendRequest(readCO2);
  
  unsigned long ppm = getValue(response);
  client.write(response, 7);
  Serial.print(response[0], HEX);Serial.print(response[1], HEX);Serial.print(response[2], HEX);Serial.print(response[3], HEX);Serial.print(response[4], HEX);Serial.print(response[5], HEX);Serial.print(response[6], HEX);
  Serial.print("Co2 ppm = ");
  Serial.println(ppm);
}

void awaitPoll()
{
  while(client.available() < 7);

  for (int i=0; i < 7; i++)
  {
    serverData[i] = client.read();
  }
}

void sendRequest(byte packet[])
{
  sensorSerial.write(readCO2, 7);
  //client.write(sensorSerial.available() );
  delay(50);
  

  int timeout=0;  //set a timeoute counter
  while(sensorSerial.available() < 7 ) //Wait to get a 7 byte response
  {
    timeout++;  
    if(timeout > 10)    //if it takes to long there was probably an error
      {
        while(sensorSerial.available())  //flush whatever we have
          sensorSerial.read();
          
          break;                        //exit and try again
      }

      delay(50);
  }
  for (int i=0; i < 7; i++)
  {
    response[i] = sensorSerial.read();
  } 
}

unsigned long getValue(byte packet[])
{
  int high = packet[3];
  int low = packet[4];

  unsigned long val = high*256 + low;
  return val;
}
