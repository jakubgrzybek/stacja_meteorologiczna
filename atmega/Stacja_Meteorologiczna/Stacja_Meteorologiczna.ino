//LIBS
#include <Wire.h>
#include <SPI.h>

//PINS
#define LED                 7    // pin number for LED
#define RAIN                A0   // analog pin number for rain check
//#define ADDITIONAL_PIN_1  A2   // additional analog pin
//#define ADDITIONAL_PIN_2  A4   // additional analog pin
#define PIN_LED             10   // pin number - internal led for pm measurement
#define PIN_ANALOG          A5   // pin number - pm measurement
#define MIN_VOLTAGE         600  // mv - bottom treshold for pm measurement (pure air)
#define VREF                5000 // mv - reference voltage
#define MAX_ITERS           10   // number of pm measurements for average value

//VARIABLES
float   VOLTAGE;
int     ITER;      
float   ADC_VALUE;
float   DUST;
String  FLAG;
float   AVG_DUST;

//FLAGS
String cmdRain  = "rain";
String cmdPM    = "pm";

//FUNCTIONS
float measureRain()
{
  return analogRead(RAIN);
}

// computeDust, measurePM; based on sample code from: https://abc-rc.pl/product-pol-7533-Czujnik-Pylu-GP2Y1010AU0F-PM2-5-monitor-czystosci-powietrza.html

float computeDust()
{
  digitalWrite(PIN_LED, HIGH);
  delayMicroseconds(280);
  ADC_VALUE = analogRead(PIN_ANALOG);
  digitalWrite(PIN_LED, LOW);

  VOLTAGE = (VREF / 1024.0) * ADC_VALUE;
 
  if (VOLTAGE > MIN_VOLTAGE)
  {
    return (VOLTAGE - MIN_VOLTAGE) * 0.2;
  }
  return 0;
}

float measurePM()
{
   AVG_DUST = 0;
   ITER = 0;
   
   while (ITER < MAX_ITERS)
   {
    
     DUST = computeDust();
     
     if (DUST > 0)
     {
       AVG_DUST += DUST;
       ITER++;
       delay(50);
     }     
   } 
   return AVG_DUST / MAX_ITERS;
}

//BEAM LED
void beam(){
  digitalWrite(LED, HIGH);
}

//BLINK LED
void blink(int val)
{
  digitalWrite(LED, LOW);
  for(int i = 0; i < val; i++) {
    digitalWrite(LED, HIGH);
    delay(50);
    digitalWrite(LED, LOW);
    delay(50);
    beam();
  }
}

//DATA SENDER
void sendData(float value)
{
  Serial.println(value);
}

//SETUP
void setup() {
  analogReference(INTERNAL);
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);
  beam();
}

//MAIN LOOP

  //FLAGS:
  //cmdRain = "rain";
  //cmdPM   = "pm";

void loop() {
  FLAG = Serial.readString();
  if(FLAG == cmdRain) {
    blink(5);
    sendData(measureRain());
  } else if(FLAG == cmdPM) {
    blink(6);
    sendData(measurePM());
  }
}  
