# NUCLEO-F767ZI

## content

---

## info

```bash
linux:~ # lsusb

linux:~ # st-info --version
linux:~ # st-info --probe
linux:~ # st-info --serial

linux:~ # st-flash write <fw>.bin 0x8000000       # write flash
linux:~ # st-flash read <fw>.bin 0x8000000 4096   # read flash
linux:~ # st-flash erase                          # erase flash
```

---

## led

```bash
linux:~/proj # vi Core/Src/main.c
    while (1)
    {
      /* USER CODE END WHILE */

      /* USER CODE BEGIN 3 */
	    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_14, GPIO_PIN_RESET);
	    HAL_GPIO_TogglePin(BlueLED_GPIO_Port, BlueLED_Pin);
	    HAL_Delay(250);

	    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_14, GPIO_PIN_SET);
	    HAL_GPIO_TogglePin(BlueLED_GPIO_Port, BlueLED_Pin);
	    HAL_Delay(250);
    }
    /* USER CODE END 3 */

linux:~/proj # vi Core/Inc/main.h
#define RedLED_Pin GPIO_PIN_14
#define RedLED_GPIO_Port GPIOB
...

#define BlueLED_Pin GPIO_PIN_7
#define BlueLED_GPIO_Port GPIOB

linux:~/proj # make
linux:~/proj # ls build/proj.bin
linux:~/proj # st-flash write build/led.bin 0x8000000
```
