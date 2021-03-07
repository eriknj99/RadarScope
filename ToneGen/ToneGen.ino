
int freq = 0;
int dir = 0;
void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
  tone(14, freq);
  if(dir == 0){
    freq++;
    if(freq >= 1000){
      dir = 1;
    }
  }else{
    freq--;
    if(freq <= 1){
      dir = 0;
    }
  }
  delay(50);

}
