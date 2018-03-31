#define LED_1 8
#define LED_2 11

#define MOTOR_A_1 5
#define MOTOR_A_2 10

#define MOTOR_B_1 6
#define MOTOR_B_2 9

#define PROG_LED 13

struct MotorData{
  int pin1;
  int pin2;
}motorLeft, motorRight;

bool led1On = false;
bool led2On = false;
bool progLedOn = false;

bool ledToggleOn = true;
long ledToggleTime = 1000;

//mspeed of motor
int mspeed = 10;

//previous button pressed
char prevButton = ' ';

void ledsSetup(){
  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);
  pinMode(PROG_LED, OUTPUT);

  ledsSet(false, false);
}

void ledSet(int pin, bool on){
  if(on){
    digitalWrite(pin, HIGH);  
  }else{
    digitalWrite(pin, LOW);  
  }
}

void ledsSet(bool firstOn, bool secondOn){
  ledSet(LED_1, firstOn);
  ledSet(LED_2, secondOn);

  led1On = firstOn;
  led2On = secondOn;
}

void ledsToggleFast(){
  ledToggleTime = 200;
}

void ledsToggleSlow(){
  ledToggleTime = 1000;
}

void ledsToggle(){
  static long lastToggle = 0;
  static bool firstOn = false;
  static bool secondOn = false;
  
  if(!ledToggleOn){
    return;
  }
  
  if((millis() - lastToggle) >= ledToggleTime){
    lastToggle = millis();

    firstOn = !firstOn;
    secondOn = !secondOn;
    progLedOn = !progLedOn;

    ledSet(LED_1, (firstOn && led1On));
    ledSet(LED_2, (secondOn && led2On));

    ledSet(PROG_LED, progLedOn);
  }
}

void motorSetup(MotorData motor){
  pinMode(motor.pin1, OUTPUT);
  pinMode(motor.pin2, OUTPUT);

  motorBrake(motor);
}

//sets motor mspeed in forward direction
void motorForward(MotorData motor, int mspeed){
  analogWrite(motor.pin1, mspeed);
  analogWrite(motor.pin2, 0);
}

//sets motor mspeed in backward direction
void motorBackward(MotorData motor, int mspeed){
  analogWrite(motor.pin1, 0);
  analogWrite(motor.pin2, mspeed);
}

//turns off motors
void motorBrake(MotorData motor){
  digitalWrite(motor.pin1, LOW);
  digitalWrite(motor.pin2, LOW);
}

//sets both motors forward
void robotForward( int mspeed){
  motorForward(motorLeft, mspeed);
  motorForward(motorRight, mspeed);

  ledsToggleFast();
  ledsSet(true, true);
}

//sets both motors backward
void robotBackward( int mspeed){
  motorBackward(motorLeft, mspeed);
  motorBackward(motorRight, mspeed);

  ledsSet(false, false);
}

//sets left motor forward and right motor backward
void robotLeft( int mspeed){
  motorBackward(motorLeft, mspeed);
  motorForward(motorRight, mspeed);

  ledsToggleFast();
  ledsSet(true, false);
}

//sets right motor forward and left motor backward
void robotRight( int mspeed){
  motorForward(motorLeft, mspeed);
  motorBackward(motorRight, mspeed);

  ledsToggleFast();
  ledsSet(false, true);
}

//turns off both motors
void robotBrake(){
  motorBrake(motorLeft);
  motorBrake(motorRight);

  ledsToggleSlow();
  ledsSet(true, true);
}

void setup() {
  Serial.begin(9600);
  
  motorLeft.pin1 = MOTOR_A_1;
  motorLeft.pin2 = MOTOR_A_2;

  motorRight.pin1 = MOTOR_B_1;
  motorRight.pin2 = MOTOR_B_2;

  ledsSetup();

  motorSetup(motorLeft);
  motorSetup(motorRight);

  robotBrake();
}

void loop() {
  if(Serial.available() > 0){
    char direction = Serial.read();
    Serial.flush();

    //Longer the button is pressed, the faster it accelerates
    switch(direction){
      case 'a':{
        //if prevButton doesn't match current button change mspeed to 0
        if(direction != prevButton){
          mspeed = 90;
        }
        robotLeft(mspeed);
        if(mspeed >= 235){
          mspeed = 255;
        }
        else{
          mspeed = mspeed + 20;
        }
               
      }break;  

      case 'w':{
        //if prevButton doesn't match current button change mspeed to 0
        if(direction != prevButton){
          mspeed = 90;
        }
        robotForward(mspeed);
        if(mspeed >= 235){
          mspeed = 255;
        }
        else{
          mspeed = mspeed + 20;
        }
      
      }break;

      case 's':{
        //if prevButton doesn't match current button change mspeed to 0
        if(direction != prevButton){
          mspeed = 90;
        }
        robotBackward(mspeed);
        if(mspeed >= 235){
          mspeed = 255;
        }
        else{
          mspeed = mspeed + 20;
        }
      
      }break;

      case 'd':{
        //if prevButton doesn't match current button change mspeed to initial mspeed
        if(direction != prevButton){
          mspeed = 90;
        }
        robotRight(mspeed);
        if(mspeed >= 235){
          mspeed = 255;
        }
        else{
          mspeed = mspeed + 20;
        }
      
      }break;

      default:{
        robotBrake();  
      }
    }

    //set prevButton to current button
    prevButton = direction;
  }
  
  ledsToggle();
}


//Looking to add 
//motor stop when not pressed
//Mapping controls to a gamepad controller
