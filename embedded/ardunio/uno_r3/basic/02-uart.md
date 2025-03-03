# uart

## print

```cpp
void setup() {
    Serial.begin(9600);
    while(!Serial) {
      ;
    }
    Serial.print("setup\n");
  }

  void loop() {
    Serial.println("hello arduino");
    delay(1000);
  }
```

---

## read

```cpp
char receivedChar;

void setup()
{
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
    if (Serial.available() > 0) {
        receivedChar = Serial.read();
    }

    if (receivedChar == '1') {
        digitalWrite(LED_BUILTIN, HIGH);
        Serial.println("turn on");
    }
    else if(receivedChar == '0'){
        digitalWrite(LED_BUILTIN, LOW);
        Serial.println("turn off");
    }
}
```
