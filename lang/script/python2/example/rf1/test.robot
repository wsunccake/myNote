*** Settings ***
Library     OperatingSystem
Library     UserDefinePython
Resource    UserDefineRF.robot
Resource    RFVar.txt

*** Test Cases ***
Say Somethings
    Log  Hi
    RF Say  Hi Robotframe
    RF Say  ${rf_words}
    Py Say  Hi Python
    Py Say  ${py_words}