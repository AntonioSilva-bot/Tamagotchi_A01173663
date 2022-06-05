#define PIN_BOT1 3
#define PIN_BOT2 4
#define PIN_BOT3 5
int val1 = 0;
int val2 = 0;
int val3 = 0; 

void setup() {
  Serial.begin(115200);
  delay(30);
  pinMode(PIN_BOT1, INPUT);
  pinMode(PIN_BOT2, INPUT);
  pinMode(PIN_BOT3, INPUT);
}
 
void loop(){
  val1 = digitalRead(PIN_BOT1);  //lectura digital de pin
  val2 = digitalRead(PIN_BOT2);  //lectura digital de pin
  val3 = digitalRead(PIN_BOT3);  //lectura digital de pin
  if (val1 == HIGH) {
      Serial.println("uno");
  }
  if (val2 == HIGH) {
      Serial.println("dos");
  }
  if (val3 == HIGH) {
      Serial.println("tres");
  }  
  delay(250);
}
