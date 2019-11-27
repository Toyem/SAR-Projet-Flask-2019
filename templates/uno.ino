// Code changement de fréquence Arduino

#if  defined(__AVR_ATmega2560__)
void setPwmFrequencyMEGA2560(int pin, int divisor) {
  byte mode;
      switch(divisor) {
      case 1: mode = 0x01; break;
      case 2: mode = 0x02; break;
      case 3: mode = 0x03; break;
      case 4: mode = 0x04; break;
      case 5: mode = 0x05; break;
      case 6: mode = 0x06; break;
      case 7: mode = 0x07; break;
      default: return;
      }

        switch(pin) {
      case 2:  TCCR3B = TCCR3B  & 0b11111000 | mode; break;
      case 3:  TCCR3B = TCCR3B  & 0b11111000 | mode; break;
      case 4:  TCCR0B = TCCR0B  & 0b11111000 | mode; break;
      case 5:  TCCR3B = TCCR3B  & 0b11111000 | mode; break;
      case 6:  TCCR4B = TCCR4B  & 0b11111000 | mode; break;
      case 7:  TCCR4B = TCCR4B  & 0b11111000 | mode; break;
      case 8:  TCCR4B = TCCR4B  & 0b11111000 | mode; break;
      case 9:  TCCR2B = TCCR0B  & 0b11111000 | mode; break;
      case 10: TCCR2B = TCCR2B  & 0b11111000 | mode; break;
      case 11: TCCR1B = TCCR1B  & 0b11111000 | mode; break;
      case 12: TCCR1B = TCCR1B  & 0b11111000 | mode; break;
      case 13: TCCR0B = TCCR0B  & 0b11111000 | mode; break;
      default: return;
    }

}

  #endif

/*VAR POLOLU*/

int OUT9_D = 9;
int OUT10_G = 10;
int OUT52_ENG = 52;
int OUT53_END = 53;
int OUT50_INVG = 50;
int OUT51_INVD = 51;
//int input; // Variable servant à récupérer les données reçues

/* VAR XBEE*/

byte input;
byte acquisition[9];
int i = -1;
byte vitessed = 0;
byte vitesseg = 0;
byte invg;
byte invd;

/* VAR DrDAC

int CinqV_G = 38;
int CinqV_D = 39;
int IN26_A_D = 26;
int IN27_B_D = 27;
int IN24_A_G = 24;
int IN25_B_G = 25;
*/

/* VAR IR */

const int IRpin = A15;
int value1;

boolean check;

void setup() {
  // Set la frequency
  setPwmFrequencyMEGA2560(OUT9_D,1);
  setPwmFrequencyMEGA2560(OUT10_G,1);
  Serial.begin(9600); // initialisation de la connexion
  // Pin Pololu
  pinMode(OUT9_D, OUTPUT);
  pinMode(OUT10_G, OUTPUT);
  pinMode(OUT50_INVG, OUTPUT);
  pinMode(OUT51_INVD, OUTPUT);
  pinMode(OUT52_ENG, OUTPUT);
  pinMode(OUT53_END, OUTPUT);

  // Pin XBee
  pinMode(LED_BUILTIN,13);
  //input = (int) 0;
  memset(&acquisition,(int)0,sizeof(char)*5);

  /*Pin DrDAC
  pinMode(CinqV_G, INPUT);
  pinMode(CinqV_D, INPUT);
  pinMode(IN26_A_D, INPUT);
  pinMode(IN27_B_D, INPUT);
  pinMode(IN24_A_G, INPUT);
  pinMode(IN25_B_G, INPUT);
  */
}

void loop() {

  // Code Capteur IR
  // Serial.println(irRead(), DEC);
  float volts = analogRead(IRpin)*0.0048828125;
  float distance=32*pow(volts,-1.10);
  //Serial.print(distance);
  if(distance < 20 ){
    digitalWrite(OUT52_ENG, LOW);
    digitalWrite(OUT53_END, LOW);
    //Serial.print("STOP");
  }else{
    digitalWrite(OUT52_ENG, HIGH);
    digitalWrite(OUT53_END, HIGH);
  }

  // Code lancement XBee
  if(Serial.available()){
    input = Serial.read ();
    Serial.print("----input-----");
    Serial.println();
    Serial.print(input);
    Serial.println();
    /*
    if(input == 91 or input == 93 or input == 59){
      input == (char)input;
    }

    Serial.print("tu marche :");
    Serial.print(input);
    Serial.println();
    */
    // Code Xbee
    if(i<9){
      i=i+1;
      acquisition[i] = input;
      /*
      Serial.print("i :");
      Serial.print(i);
      Serial.println();
      Serial.print("aq in loop : ");
      Serial.print(acquisition[i]);
      Serial.println();
      */
      //input = (int) 0;
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(5);                          // wait for a second
      digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
      delay(5);
    }
    if(i>=8){
      if (acquisition[0] == 91 and acquisition[2]==59 and acquisition[4]==59 and acquisition[8]==93){
          check = true;
      for(int j=0;j<8;j++){
        if (j==1){
          vitessed = acquisition[j];
        }
        if (j==3){
          vitesseg = acquisition[j];
        }
        if (j==5){
          invd= acquisition[j];
        }
        if (j==7){
          invg=acquisition[j];
        }
      }
      Serial.print("----aquisition-----");
      Serial.println();
      Serial.print((int)acquisition);
      Serial.println();
      Serial.print(check);
      Serial.println();
      i=-1;
      // Code Pololu
      if (invd==1){
        //Serial.print("#invd if");
        digitalWrite(OUT51_INVD,LOW); // HIGH=Avancer
      }else{
        digitalWrite(OUT51_INVD,HIGH); // HIGH=Avancer
      }
      if (invg==1){
        //Serial.print("#invg if");
        digitalWrite(OUT50_INVG,LOW); // HIGH=Avancer
        //invg = 0;
      }else{
        //Serial.print("#invg else");
        digitalWrite(OUT50_INVG,HIGH); // HIGH=Avancer
      }
      analogWrite(OUT9_D,vitessed); // Vitesse roue droite
      analogWrite(OUT10_G,vitessed); // Vitesse roue gauche
      //digitalWrite(OUT52_ENG, HIGH); // HIGH=Avancer
      //digitalWrite(OUT53_END, HIGH); // HIGH=Avancer

     /**
      * SI INV = LOW alors la partie du moteur avance
      *
      */
    }else{
          i = -1;
          check = false;
         }
    }
    /*
    // Code DrDac
    // Mesure la durée de l'impulsion haute sur A (timeout par défaut de 1s)
    noInterrupts();
    unsigned long etat_haut_A_D = pulseIn(IN26_A_D, HIGH);
    interrupts();
    // Mesure la durée de l'impulsion basse (timeout par défaut de 1s)
    noInterrupts();
    unsigned long etat_bas_A_D = pulseIn(IN26_A_D, LOW);
    interrupts();
    // Calcul de la periode = etat haut + etat bas
    long period_A_D = (etat_bas_A_D + etat_haut_A_D);
    // Calcul de la frequence = 1 / periode
    long frequence_A_D = (1/ (period_A_D*0.000001));
    // Calcul du tour/sec
    long tour_sec_A_D = frequence_A_D/500;
    // distance par sec
    long distance_sec_A_D = 2*3.1415*0.04*tour_sec_A_D;


    //---------------------------------------

    // Mesure la durée de l'impulsion haute sur B (timeout par défaut de 1s)
    noInterrupts();
    unsigned long etat_haut_B_D = pulseIn(IN27_B_D, HIGH);
    interrupts();
    // Mesure la durée de l'impulsion basse (timeout par défaut de 1s)
    noInterrupts();
    unsigned long etat_bas_B_D = pulseIn(IN27_B_D, LOW);
    interrupts();
    // Calcul de la periode = etat haut + etat bas
    long period_B_D = (etat_bas_B_D + etat_haut_B_D);
    // Calcul de la frequence = 1 / periode
    long frequence_B_D = (1/ (period_B_D*0.000001));
    // Calcul du tour/sec
    long tour_sec_B_D = frequence_B_D/500;
    // distance par sec
    long distance_sec_B_D = 2*3.1415*0.04*tour_sec_B_D;


    Serial.println("----------------");
    Serial.println("----------------");
    Serial.println("----#######-----");
    Serial.println("----------------");
    Serial.println("----------------");

    Serial.println("Frequence A: ");
    Serial.print(frequence_A_D);
    Serial.println(" Hz");
    Serial.println("");
    Serial.println("Frequence B: ");
    Serial.print(frequence_B_D);
    Serial.println(" Hz");
    Serial.println("");

    delay(500);
    */
  }
}

int irRead() {
  int averaging = 0;
  for (int i=0; i<5; i++) {
    value1 = analogRead(IRpin);
    averaging = averaging + value1;
  }
  value1 = averaging / 5;
  return(value1);
}