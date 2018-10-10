//This code runs from the particle cloud and manages the Raspberry Pi using IoT

int M = D0; //GPIO6
int F = D1; //GPIO21
int U = D2; //GPIO22
int L = D3; //GPIO24
int I = D4; //GPIO25
int P = D5; //GPIO12



// setup() is run only once, it's where we set up GPIO and initialize peripherals
void setup() {
    
  // Setup GPIO
  pinMode(M,OUTPUT); // MEDIUM
  pinMode(F,OUTPUT); // FREEZING
  pinMode(U,OUTPUT); // HUMID 
  pinMode(L,OUTPUT); // CLOUDY
  pinMode(I,OUTPUT); // WINDY
  pinMode(P,OUTPUT); // DEFINITE RAIN
  //Initializing everything to be off
  digitalWrite(M,LOW);
  digitalWrite(F,LOW);
  digitalWrite(U,LOW);
  digitalWrite(L,LOW);
  digitalWrite(I,LOW);
  digitalWrite(P,LOW);
  
  // Subscribe to an event published by IFTTT using Particle.subscribe
  Particle.subscribe("unique_event_name", myHandler);
  // Subscribe will listen for the event unique_event_name and, when it finds it, will run the function myHandler()
  // (Remember to replace unique_event_name with an event name of your own choosing. Make it somewhat complicated to make sure it's unique.)
  // myHandler() is declared later in this app.
}

// loop() runs continuously, it's our infinite loop. In this program we only want to repsond to events, so loop can be empty.
void loop() {

}

// Now for the myHandler function, which is called when the Particle cloud tells us that our email event is published.
void myHandler(const char *event, const char *data)
{

  if (strstr(data,"P")!=NULL) {
    // if subject line of email is "off"
    digitalWrite(P,HIGH);
    //digitalWrite(P,LOW);
  }
  else if (strstr(data,"G")!=NULL) {
    // if subject line of email is "off"
    digitalWrite(P,HIGH);
    //digitalWrite(P,LOW);
  }
  else{
      digitalWrite(P,LOW);
  }
  
  if (strstr(data,"I")!=NULL) {
    // if subject line of email is "off"
    digitalWrite(I,HIGH);
    //digitalWrite(P,LOW);
  }
  else{
      digitalWrite(I,LOW);
  }
  if (strstr(data,"L")!=NULL) {
    // if subject line of email is "off"
    digitalWrite(L,HIGH);
    //digitalWrite(P,LOW);
  }
  else{
      digitalWrite(L,LOW);
  }
  
  if (strstr(data,"U")!=NULL) {
    // if subject line of email is "off"
    digitalWrite(U,HIGH);
    //digitalWrite(P,LOW);
  }
  else{
      digitalWrite(U,LOW);
  }
  if (strstr(data,"F")!=NULL) {
    // if subject line of email is "off"
    digitalWrite(F,HIGH);
    if(strstr(data,"P")!=NULL){
        digitalWrite(M,HIGH);
    }
    //digitalWrite(P,LOW);
  }
  else{
      digitalWrite(F,LOW);
  }
  if (strstr(data,"C")!=NULL) {
    // if subject line of email is "off"
    digitalWrite(F,HIGH);
    //digitalWrite(P,LOW);
  }
  
}