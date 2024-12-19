
//Declare Motor Pins
#define IN1A 10   //  IN1 IN2
#define IN2A 11  //  PWM 0   |Forward
#define IN1B 5    //  0   PWM |Reverse
#define IN2B 6    //  1   1   |Brake
// 20

//Hardware measurements
#define maxRPM 20
const float baseDistance = 0.2; //distance between wheels in metres
const float wheelDiameter = 0.15; //diameter of wheel

const float baseHalf = baseDistance/2;
const float wheelRadius = wheelDiameter/2;
const float distPerRev = wheelDiameter*PI; //dist per rev of wheel


float rightVel = 0.0; //Velocity of right wheel
float leftVel = 0.0; //Velocity of left wheel
float rightRpm = 0.0;
float leftRpm = 0.0;
float rightPwm = 0.0;
float leftPwm = 0.0;

//====== Serial Stuff
const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

      // variables to hold the parsed data
char messageFromROS[numChars] = {0};
float angularVel = 0.0;
float linearVel = 0.0;
boolean newData = false;
//============

char fuden[] = "hello world";

void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
  //Serial.println("<HelloWorld, 0.15, 0>");
  //Innit Motor Pins
  pinMode(IN1A, OUTPUT);
  pinMode(IN2A, OUTPUT);
  pinMode(IN1B, OUTPUT);
  pinMode(IN2B, OUTPUT); 
  delay(10);
  digitalWrite(IN1A, LOW);
  digitalWrite(IN1B, LOW);

  
}

void loop() {

readSerial();
calVel();
//    <v, 0.15, 0>
timer();
moveWheels();

}
//============================================
unsigned long startMillis = millis();  //some global variables available anywhere in the program
unsigned long currentMillis;
const unsigned long period = 1000;
void timer(){
  currentMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started)
  if (currentMillis - startMillis >= period)  //test whether the period has elapsed
  {
    //Serial.println((float)leftRpm);
    //Serial.println((float)leftPwm);



    startMillis = currentMillis;  //IMPORTANT to save the start time of the current LED state.
  }
}

void readSerial(){
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        //showParsedData();
        newData = false;
    }
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");      // get the first part - the string
    strcpy(messageFromROS, strtokIndx); // copy it to messageFromPC
 
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    linearVel = atof(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ",");
    angularVel = atof(strtokIndx);     // convert this part to a float

}

//============
float x = 0.0;

void showParsedData() {
    Serial.print("Message ");
    Serial.println(messageFromROS);
    Serial.print("Integer ");
    Serial.println(linearVel);
    Serial.print("Float ");
    Serial.println(angularVel);
    x = angularVel + linearVel;
    Serial.println(x);
    
}

float pwmMap(float y){
  x = abs(y);
  //cap max rpm
  if(x >= 20.0){
    return 254;
    }
  else{ 
  return (x * (254 / maxRPM));
}}
void calVel(){
 
  leftVel = linearVel + (angularVel * baseHalf);
  rightVel = linearVel - (angularVel * baseHalf);
  //Calculate pwm to send to each motor
  leftRpm = leftVel * (60 / distPerRev);
  rightRpm = rightVel * (60 / distPerRev);
  leftPwm = pwmMap(leftRpm);
  rightPwm = pwmMap(rightPwm); 
}

void moveWheels(){
  //brake
  if( linearVel == 0.0 and angularVel == 0.0){
    digitalWrite(IN1A,HIGH);
    digitalWrite(IN2A, HIGH);
    digitalWrite(IN1B,HIGH);
    digitalWrite(IN2B, HIGH);
  }
  else{

    //_____LEFT wheel_________
  if( leftRpm > 0.0){//forwards
    analogWrite(IN1A,leftPwm);
    digitalWrite(IN2A, LOW);
    }
   else{//reverse
    analogWrite(IN2A,leftPwm);
    digitalWrite(IN1A, LOW);
   }
   
//_____RIGHT wheel_________
  if( rightRpm > 0.0){//forwards
    analogWrite(IN1B,leftPwm);
    digitalWrite(IN2B, LOW);
    }
   else{//reverse
    analogWrite(IN2B,leftPwm);
    digitalWrite(IN1B, LOW);
   }
  }


   
}
