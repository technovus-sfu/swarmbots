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
void motorForward(MotorData motor, int motorValue){
  analogWrite(motor.pin1, motorValue);
  analogWrite(motor.pin2, 0);
}

//sets motor mspeed in backward direction
void motorBackward(MotorData motor, int motorValue){
  analogWrite(motor.pin1, 0);
  analogWrite(motor.pin2, motorValue);
}

//turns off motors
void motorBrake(MotorData motor){
  digitalWrite(motor.pin1, LOW);
  digitalWrite(motor.pin2, LOW);
}

//turns off motors
void robotBrake(){
  motorBrake(motorLeft);
  motorBrake(motorRight);

  ledsToggleSlow();
  ledsSet(true, true);
}

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);
  motorLeft.pin1 = MOTOR_A_1;
  motorLeft.pin2 = MOTOR_A_2;

  motorRight.pin1 = MOTOR_B_1;
  motorRight.pin2 = MOTOR_B_2;

  ledsSetup();

  motorSetup(motorLeft);
  motorSetup(motorRight);

  robotBrake();
}

byte cmd[2];
bool cmdready = false;

void recieveBytes(){
  static byte i = 0;
  if(Serial.available() > 0 && cmdready == false){
    cmd[i] = Serial.read();
    i++; 
    if(i >= 2){
      i = 0;
      cmdready = true;
    }
  }
}

void loop() {

  recieveBytes();

  if (cmdready){
    cmdready = false;
    //command numbering is the same as the numbering of the quadrants in a graph
    switch(cmd[0]){
      case 1:{ //right motor forward
        //controlling forward speed of right motor
        motorForward(motorRight, cmd[1]);
        
      }break;  

      case 2:{ //left motor forward
        //controlling forward speed of left motor
        motorForward(motorLeft, cmd[1]);
      
      }break;

      case 3:{ //left motor backward
      //controlling backward speed of left motor
        motorBackward(motorLeft, cmd[1]); 
            
      }break;

      case 4:{ //right motor backward
      //controlling backward speed of right motor
        motorBackward(motorRight, cmd[1]);
      
      }break;
    }
  }
  ledsToggle();
}

