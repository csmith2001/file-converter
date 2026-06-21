@echo off
@REM Windows Setup Script

set SCRIPT_DIR=%~dp0

@REM cd one level up to project root
cd /d "%SCRIPT_DIR%.."
set PROJECT_DIR=%CD%

echo.
echo Project Directory: %PROJECT_DIR%
echo Script Directory: %SCRIPT_DIR%
echo.

@REM Check for Python Venv
echo Checking for Python Virtual Environment...
set VENV_DIR=%PROJECT_DIR%\.venv
set VENV=%VENV_DIR%\Scripts\python.exe

if not exist "%VENV_DIR%" (
    echo.
    echo Creating .venv
    python -m venv "%VENV_DIR%"
    echo.
    echo Upgrading pip
    "%VENV%" -m pip install --upgrade pip
) else (
    echo .venv exists
)

@REM Install requirements.txt
set REQ_FILE=%PROJECT_DIR%\requirements.txt
set REQ_LOG=%VENV_DIR%\installed.txt
set SETUP_LOG=%TEMP%\file_converter_setup_log.txt
set SETUP_FILTER=Collecting Installing Successfully Requirement

if not exist "%REQ_FILE%" (
    echo WARNING: requirements.txt not found
) else (
    echo.
    echo Installing dependencies...

    @REM Install requirements.txt, output to temp log
    "%VENV%" -m pip install -r "%REQ_FILE%" --disable-pip-version-check > "%SETUP_LOG%" 2>&1

    @REM Filter temp log to capture relevant info
    for /f "tokens=*" %%a in ('findstr "%SETUP_FILTER%" "%SETUP_LOG%"') do (
        for /f "tokens=1,2,3,4" %%w in ("%%a") do (
            if "%%w"=="Requirement" (
                echo %%w %%y %%z
            ) else if "%%w"=="Collecting" (
                echo %%w %%x
            ) else if "%%w"=="Installing" (
                echo.
                echo %%a
            ) else (
                echo %%a
            )
        )
    )

    @REM Delete temp log
    if exist "%SETUP_LOG%" del /f /q "%SETUP_LOG%"
)

echo.
echo ================================
echo Setup Complete!
echo To activate run: %VENV_DIR%\Scripts\activate.bat
echo ================================
echo.
pause

:: NOTES

:: ^ = line continuation, i.e. split one command across multiple lines
:: | = pipe output from left command to right command

:: %~dp0
:: %0 = path to script, depends on how script was run
:: ~ = removes quotes and enables modifiers
:: d = drive of script
:: p = path of script, directory only no filename
:: %~dp0 = full absolute path to this script's directory
:: %0 may be relative (setup.bat) or absolute (C:\path\setup.bat)

:: .. = parent directory, i.e. go up one level
:: cd = change directory
:: /d = change drive
:: cd /d = change drive AND directory

:: for /f = tokenize string into chunks. Default separator is space
:: tokens=1,2,3,4 = assign 4 tokens to variables
:: ^| = the pipe must be escaped because it is inside a for /f command. ^ does so because it is not followed by a new line immediately.