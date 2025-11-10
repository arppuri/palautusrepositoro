*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  kale
    Set Password  kalle123
    Set Passwordconfirmation    kalle123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  ka
    Set Password  kalle123
    Set Passwordconfirmation    kalle123
    Click Button  Register
    Register Should Fail With Message    Username is too short

Register With Valid Username And Too Short Password
    Set Username  ale
    Set Password  kalle12
    Set Passwordconfirmation    kalle12
    Click Button  Register
    Register Should Fail With Message    Password is too short


Register With Nonmatching Password And Password Confirmation
    Set Username  kall
    Set Password  kalle123
    Set Passwordconfirmation    kalleka234
    Click Button  Register
    Register Should Fail With Message    Password does not match

Register With Valid Username And Invalid Password
    Set Username  kall
    Set Password  kallekalle
    Set Passwordconfirmation    kallekalle
    Click Button  Register
    Register Should Fail With Message    Password must contain at least 1 digit

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Passwordconfirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page