# NUCLEO-L476RG

## LED

```text
System Core \ GPIO

            pin     GPIO mode           GPIO output level
Green LED : PA5  -> Output Push Pull    Low
```

```c
// Core/Src/main.c
...
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
    HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_SET);
    HAL_Delay(1000);
    HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);
    HAL_Delay(1000);
  }
  /* USER CODE END 3 */
```

```c
// Core/Inc/main.h
...
/* Private defines -----------------------------------------------------------*/
#define LD2_Pin GPIO_PIN_5
#define LD2_GPIO_Port GPIOA
```

---

## Push-buttons

```text
System Core \ GPIO

              pin     GPIO mode           GPIO output level
Green LED   : PA5  -> Output Push Pull    Low
User Button : PC13 -> Input mode
```

```c
// Core/Src/main.c
...
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
    if (!HAL_GPIO_ReadPin(B1_GPIO_Port, B1_Pin))
    {
      HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_SET);
    }
    else
    {
      HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);
    }
  }
  /* USER CODE END 3 */
```

```c
// Core/Inc/main.h
...
/* Private defines -----------------------------------------------------------*/
#define B1_Pin GPIO_PIN_13
#define B1_GPIO_Port GPIOC
#define LD2_Pin GPIO_PIN_5
#define LD2_GPIO_Port GPIOA
```

---

## USART

```text
Connectivity \ USART2
  Mode Asynchronous

              pin     GPIO mode           GPIO output level
Green LED   : PA5  -> Output Push Pull    Low
User Button : PC13 -> Input mode
```

USART2: PA2(TX), PA3(RX)
ON: SB13, SB14 --- OFF: SB62, SB63
