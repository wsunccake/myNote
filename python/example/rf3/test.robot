*** Settings ***
Library     OperatingSystem
Library     SSHLibrary  WITH NAME  SSH

*** Variables ***
${HOST}  127.0.0.1
${USERNAME}  root
${PASSWORD}  password

*** Keywords ***
SSH Login
    [Arguments]    ${host}=${HOST}  ${username}=${USERNAME}  ${password}=${PASSWORD}
    Open Connection  ${host}
    Login  ${username}  ${password}

SSH Logout
    Close Connection

Run ${cmd} Command
    Write  ${cmd}
    ${stdout}=  Read
    Log  ${stdout}

Run ${cmd} Command With RC
    Start Command  ${cmd}
    ${stdout}  ${stderr}  ${rc}=  Read Command Output  return_stderr=True  return_rc=True
    Log  rc: ${rc}
    Log  stdout: ${stdout}
    Log  stderr: ${stderr}

*** Test Cases ***
Show Hostname
    SSH Login
    Run hostname Command
    Run ls abc Command
    Run ls abc Command With RC
    Run ls abc Command With RC
    SSH Logout