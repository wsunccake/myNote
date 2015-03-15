*** Settings ***
Library     OperatingSystem
Library     UserDefined


*** Keywords ***
Run Error Command Without Check Return Code
    [Arguments]  ${cmd}=ls /abc
    ${result}=  Run  ls /abc
    Log  result:${result}

Run Error Command With Check Return Code
    [Arguments]  ${cmd}=ls /abc
    ${rc}  ${result}=  Run and Return RC and Output  ls /abc
    Log  result:${result} rc: ${rc}
    Should Be True  ${rc} == 0

Run Python Without Check
    intAdd  4  9

Run Python With Check
    ${result}=  intAdd  ${4}  ${9}
    Should Be Equal As Integers  ${result}  ${13}

Run Python With Different Type
    intAdd  4  ${9}


*** Test Cases ***
Run Shell Command Example
    Run Error Command Without Check Return Code
    Run Error Command With Check Return Code

Run Python Example
    Run Python Without Check
    Run Python With Check
    Run Python With Different Type