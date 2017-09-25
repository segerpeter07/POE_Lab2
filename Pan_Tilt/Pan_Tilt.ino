// Sweep
// by BARRAGAN <http://barraganstudio.com> 
// This example code is in the public domain.


#include <Servo.h> 
 
Servo turn;  // create servo object to control a servo 
Servo tilt;                // a maximum of eight servo objects can be created 
 
int pos_tilt = 110;    // variable to store the servo position 
int pos_turn = 0;    // variable to store the servo position 
int sensorpin = A0;
int val = 0;

void setup() 
{ 
  turn.attach(9);  // attaches the servo on pin 9 to the servo object 
  tilt.attach(8);
  Serial.begin(9600);
} 
 
 
void loop() 
{
  if(Serial.available() >= 0 ) {
    int incoming = Serial.read();
    if(incoming == 1) {
      Start_fn();
    }
  }
}

void Start_fn()
{
  turn.write(pos_turn);
  tilt.write(pos_tilt);
  delay(100);
 for(pos_turn = 0; pos_turn < 180;) 
  {
for(pos_tilt = 110; pos_tilt < 140; pos_tilt += 1)  // goes from 0 degrees to 180 degrees 
{                                // in steps of 1 degree 
  tilt.write(pos_tilt);              // tell servo to go to position in variable 'pos' 
  delay(100);
  val = analogRead(sensorpin);
  Serial.print(pos_tilt);
  Serial.print(",");
  Serial.print(pos_turn);
  Serial.print(",");
  Serial.print(val);  
  Serial.println("");
      // waits 15ms for the servo to reach the position 
} 
    pos_turn = pos_turn + 1;
    turn.write(pos_turn);
  for(pos_tilt = 140; pos_tilt>=110; pos_tilt-=1)     // goes from 180 degrees to 0 degrees 
  {       
    tilt.write(pos_tilt);              // tell servo to go to position in variable 'pos' 
    delay(100);                       // waits 15ms for the servo to reach the position     val = analogRead(sensorpin);
    Serial.print(pos_tilt);
    Serial.print(",");
    Serial.print(pos_turn);
    Serial.print(",");
    Serial.print(val);
    Serial.println("");
  } 
  pos_turn = pos_turn +1;
  turn.write(pos_turn);
  delay(30);
    }
}

