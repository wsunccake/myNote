# robotframework-pabot

## install

```bash
linux:~ $ pip install robotframework-pabot
```

---

## usage

```robot
# sleep1s.robot
*** Test Cases ***
Wait For 1s
    [Tags]  sleep
    sleep  1
    log  hello sleep 1

Wait For 2s
    [Tags]  sleep
    sleep  2
    log  hello sleep 2
```

```robot
# sleep3s.robot
*** Test Cases ***
Wait For 3s
    [Tags]  sleep
    sleep  3
    log  hello sleep 3
```

```robot
# sleep5s.robot
*** Test Cases ***
Wait For 5s
    [Tags]  sleep
    sleep  5
    log  hello sleep 5
```

```bash
linux:~ $ robot -i sleep sleep*.robot       # run all testcase with 1 process , total sleep 1 + 2 + 3 + 5
linux:~ $ pabot -i sleep sleep*.robot       # run all testcase with 3 process , total sleep 1 + 2,  3,  5
                                            # suite level parallel
linux:~ $ pabot --processes <n> -i sleep sleep*.robot       # run all testcase with n process
linux:~ $ pabot --testlevelsplit -i sleep sleep*.robot      # run all testcase with n process, total sleep 1, 2,  3,  5
                                                            # test level parallel
```


---

## ref

[Pabot](https://pabot.org/)

[Pabot](https://github.com/mkorpela/pabot)

[PabotLib](https://pabot.org/PabotLib.html)
