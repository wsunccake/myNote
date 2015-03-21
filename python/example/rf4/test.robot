*** Settings ***
Library        Selenium2Library

*** Variables ***
${delay}=  ${1}
${google_url}=  http://www.google.com
${browser}=  firefox

*** Test Cases ***
Test Google
    Open Browser  ${google_url}  ${browser}
    Capture Page Screenshot
    Set Selenium Speed  ${delay}
    Maximize Browser Window

    Input Text  id=lst-ib  robotframework\n
    Capture Page Screenshot

    Click Link  css=#rso > div:nth-child(2) > li:nth-child(1) > div > h3 > a
    Capture Page Screenshot

    Title Should Be  Robot Framework
    ${url}=  Get Location
    Log  ${url}
    Click Link  xpath=//*[@id="menu"]/div/ul/li[1]/a
    Click Link  css=#menu > div > ul > li:nth-child(2) > a
    Close Browser