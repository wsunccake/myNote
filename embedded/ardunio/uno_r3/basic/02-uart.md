# uart

## hello

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
