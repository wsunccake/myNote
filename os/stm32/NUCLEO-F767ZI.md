# NUCLEO-F767ZI

## content

---

## info

```bash
linux:~ # lsusb
linux:~ # dmesg

linux:~ # ls /dev/ttyACM*


```

---

## led

```text
            pin     GPIO Mode
Green LED : PA5  -> Output Push Pull
Blue  LED : PB7  -> Output Push Pull
Red   LED : PB14 -> Output Push Pull
```

```bash
linux:~/proj # vi Core/Src/main.c
linux:~/proj # vi Core/Inc/main.h

linux:~/proj # make
linux:~/proj # ls build/led.bin
linux:~/proj # st-flash write build/led.bin 0x8000000
```

```c
// Core/Src/main.c
static void MX_GPIO_Init(void);

...
    while (1)
    {
      /* USER CODE END WHILE */

      /* USER CODE BEGIN 3 */
	    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_14, GPIO_PIN_SET);
	    HAL_GPIO_TogglePin(BlueLED_GPIO_Port, BlueLED_Pin);
	    HAL_GPIO_TogglePin(GreenLED_GPIO_Port, GreenLED_Pin);
	    HAL_GPIO_TogglePin(OSC_GPIO_Port, OSC_Pin);
	    HAL_Delay(1000);

	    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_14, GPIO_PIN_RESET);
	    HAL_GPIO_TogglePin(BlueLED_GPIO_Port, BlueLED_Pin);
	    HAL_GPIO_TogglePin(GreenLED_GPIO_Port, GreenLED_Pin);
	    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_7);
	    HAL_Delay(100);
    }
    /* USER CODE END 3 */
```

```c
// Core/Inc/main.h
...
#define OSC_Pin GPIO_PIN_7
#define OSC_GPIO_Port GPIOA
#define GreenLED_Pin GPIO_PIN_0
#define GreenLED_GPIO_Port GPIOB
#define RedLED_Pin GPIO_PIN_14
#define RedLED_GPIO_Port GPIOB
#define BlueLED_Pin GPIO_PIN_7
#define BlueLED_GPIO_Port GPIOB
```

---

## uart / usart

```bash
linux:~/proj # vi Core/Src/main.c
linux:~/proj # vi Core/Inc/main.h

linux:~/proj # make
linux:~/proj # ls build/uart.bin
linux:~/proj # STM32_Programmer_CLI -c port=SWD -d build/uart.bin 0x08000000 -v
linux:~/proj # STM32_Programmer_CLI -c port=SWD -hardRst

# other console
linux:~ # screen /dev/ttyACM0 115200
```

```c
// Core/Src/main.c if uart
static void MX_GPIO_Init(void);
static void MX_USART3_UART_Init(void);
...

/* USER CODE BEGIN 0 */
uint8_t buffer_uart[]= "Hello";
/* USER CODE END 0 */
...

  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
    HAL_Delay(300);
    HAL_UART_Transmit(&huart3, buffer_uart, sizeof(buffer_uart), 100);
  }
  /* USER CODE END 3 */
```

```c
// Core/Src/main.c if usart
static void MX_GPIO_Init(void);
static void MX_USART3_Init(void);
...

/* USER CODE BEGIN 0 */
uint8_t buffer_uart[]= "Hello";
/* USER CODE END 0 */
...

  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
    HAL_Delay(300);
    HAL_USART_Transmit(&husart3, buffer_uart, sizeof(buffer_uart), 100);
  }
  /* USER CODE END 3 */
```
