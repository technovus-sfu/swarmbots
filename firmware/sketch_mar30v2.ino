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

//motorSpeed of motor
int motorSpeed = 90;

//previous button pressed
char prevButton = ' ';

//stores the last time the left/right turn is called
unsigned long previousMillis = 0;

//current time in milliseconds
unsigned long currentMillis = 0;

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

//sets motor motorSpeed in forward direction
void motorForward(MotorData motor, int motorSpeed){
  analogWrite(motor.pin1, motorSpeed);
  analogWrite(motor.pin2, 0);
}

//sets motor motorSpeed in backward direction
void motorBackward(MotorData motor, int motorSpeed){
  analogWrite(motor.pin1, 0);
  analogWrite(motor.pin2, motorSpeed);
}

//turns off motors
void motorBrake(MotorData motor){
  digitalWrite(motor.pin1, LOW);
  digitalWrite(motor.pin2, LOW);
}

//sets both motors forward
void robotForward( int motorSpeed){
  motorForward(motorLeft, motorSpeed);
  motorForward(motorRight, motorSpeed);

  ledsToggleFast();
  ledsSet(true, true);
}

//sets both motors backward
void robotBackward( int motorSpeed){
  motorBackward(motorLeft, motorSpeed);
  motorBackward(motorRight, motorSpeed);

  ledsSet(false, false);
}

//sets left motor forward and right motor backward
void robotLeft( int motorSpeed){
  motorBrake(motorLeft);
  motorForward(motorRight, motorSpeed);

  previousMillis = millis();

  ledsToggleFast();
  ledsSet(true, false);
}

//sets right motor forward and left motor backward
void robotRight( int motorSpeed){
  motorForward(motorLeft, motorSpeed);
  motorBrake(motorRight);

  previousMillis = millis();

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
  //updates the current time
  currentMillis = millis();
  
  if(Serial.available() > 0){
    char direction = Serial.read();
    Serial.flush();

    //Longer the button is pressed, the faster it accelerates
    switch(direction){
      case 'a':{
        //if prevButton doesn't match current button change motorSpeed to 0
        if(direction != prevButton){
          motorSpeed = 90;
        }
        robotLeft(motorSpeed);
        if(motorSpeed >= 235){
          motorSpeed = 255;
        }
        else{
          motorSpeed = motorSpeed + 20;
        }
               
      }break;  

      case 'w':{
        //if prevButton doesn't match current button change motorSpeed to 0
        if(direction != prevButton){
          motorSpeed = 90;
        }
        robotForward(motorSpeed);
        if(motorSpeed >= 235){
          motorSpeed = 255;
        }
        else{
          motorSpeed = motorSpeed + 20;
        }
      
      }break;

      case 's':{
        //if prevButton doesn't match current button change motorSpeed to 0
        if(direction != prevButton){
          motorSpeed = 90;
        }
        robotBackward(motorSpeed);
        if(motorSpeed >= 235){
          motorSpeed = 255;
        }
        else{
          motorSpeed = motorSpeed + 20;
        }
      
      }break;

      case 'd':{
        //if prevButton doesn't match current button change motorSpeed to initial motorSpeed
        if(direction != prevButton){
          motorSpeed = 90;
        }
        robotRight(motorSpeed);
        if(motorSpeed >= 235){
          motorSpeed = 255;
        }
        else{
          motorSpeed = motorSpeed + 20;
        }
      
      }break;

      default:{
        robotBrake();  
      }
    }

    //set prevButton to current button
    prevButton = direction;
  }

  //checks if the direction is currently in the left or right direction
  //checks also if 500 milliseconds have passed since left/right button is pressed
  if(prevButton == 'a' || prevButton == 'd' && (currentMillis - previousMillis) >= 500){
    int reducedSpeed = motorSpeed - 10;
    
    //checks for left button
    if(prevButton == 'a'){
      //make left motor move forward at reduced speed
      motorForward(motorLeft, reducedSpeed);      
    }
    
    //checks for right button
    else if(prevButton == 'd'){
      //make right motor move forward at reduced speed
      motorForward(motorRight, reducedSpeed);
    }
    
  }
  
  ledsToggle();
}

