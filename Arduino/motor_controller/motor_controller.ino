#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

int m1_signal_input_pin = 2;
int m2_signal_input_pin = 3;

int m1_enable_pin = 4;

int m1_speed_pin = 5;
int m2_speed_pin = 6;

int m2_enable_pin = 7;

int m1_direction_pin = 8;
int m2_direction_pin = 9;

char drive_direction = '-';
char turn_direction = '-';

unsigned long m1_step_count = 0;
unsigned long m2_step_count = 0;

void countStepsM1() {
  m1_step_count++;
}

void countStepsM2() {
  m2_step_count++;
}

Adafruit_BNO055 bno = Adafruit_BNO055(Adafruit_BNO055::OPERATION_MODE_NDOF, 0x28);

void setup() {
  Serial.begin(19200);
  
  pinMode(m1_enable_pin, OUTPUT);
  pinMode(m1_signal_input_pin, INPUT);
  pinMode(m1_direction_pin, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(m1_signal_input_pin), countStepsM1, CHANGE);

  pinMode(m2_enable_pin, OUTPUT);
  pinMode(m2_signal_input_pin, INPUT);
  pinMode(m2_direction_pin, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(m2_signal_input_pin), countStepsM2, CHANGE);

  bno.begin();
}


void drive(char direction, int speed) {
  if (drive_direction != direction) {
    digitalWrite(m1_enable_pin, LOW);
    digitalWrite(m2_enable_pin, LOW);
    if (direction == 'f') {
      digitalWrite(m1_direction_pin, LOW);
      digitalWrite(m2_direction_pin, HIGH);
    } else if (direction == 'b') {
      digitalWrite(m1_direction_pin, HIGH);
      digitalWrite(m2_direction_pin, LOW);
    }
    drive_direction = direction;
    turn_direction = '-';
    delay(250);
  }
  analogWrite(m1_speed_pin, speed);
  analogWrite(m2_speed_pin, speed);
  
  digitalWrite(m1_enable_pin, HIGH);
  digitalWrite(m2_enable_pin, HIGH);
}

void turn(char direction) {
  if (turn_direction != direction) {
    digitalWrite(m1_enable_pin, LOW);
    digitalWrite(m2_enable_pin, LOW);
    if (direction == 'l') {
      digitalWrite(m1_direction_pin, HIGH);
      digitalWrite(m2_direction_pin, HIGH);
    } else if (direction == 'r') {
      digitalWrite(m1_direction_pin, LOW);
      digitalWrite(m2_direction_pin, LOW);
    }
    drive_direction = '-';
    turn_direction = direction;
    delay(250);
  }
  analogWrite(m1_speed_pin, 64);
  analogWrite(m2_speed_pin, 64);
  
  digitalWrite(m1_enable_pin, HIGH);
  digitalWrite(m2_enable_pin, HIGH);
}


void stop() {
  analogWrite(m1_speed_pin, 0);
  analogWrite(m2_speed_pin, 0);
  digitalWrite(m1_enable_pin, LOW);
  digitalWrite(m2_enable_pin, LOW);
}

void sendInfo() {
  sensors_event_t orientationData;
  bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  double heading = orientationData.orientation.x;
  
  String info = "I" + String(m1_step_count) + ";" + String(m2_step_count) + ";" + String(heading);
  m1_step_count = 0;
  m2_step_count = 0;
  Serial.println(info);
}

void loop() {

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    char type = command.charAt(0);
    switch (type) {
      case 's': // stop
        stop();
        Serial.println("R");
        break;
      case 'd': // drive
        drive(command.charAt(1), command.substring(2, 5).toInt());
        Serial.println("R");
        break;
      case 't': // turn
        turn(command.charAt(1));
        Serial.println("R");
        break;
      case 'i': // update
        sendInfo();
        break;
    }
  }
}
