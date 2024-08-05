@echo off
setlocal

REM 
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installe Python 3.12.
    exit /b 1
)

REM 
set modules=requests pygame astral Pillow schedule ctypes
for %%i in (%modules%) do (
    python -c "import %%i" 2>nul
    IF %ERRORLEVEL% NEQ 0 (
        echo The Python module %%i is not installed. Please install it using:
        echo pip install %%i
        exit /b 1
    )
)

REM 


REM 
set startup_folder=%AppData%\Microsoft\Windows\Start Menu\Programs\Startup
copy "%~f0" "%startup_folder%" >nul
copy "%~dp0main.py" "%startup_folder%" >nul

echo Files copied to startup folder.

pythonw "%AppData%\Microsoft\Windows\Start Menu\Programs\Startup\main.py"

echo You can close me now.
endlocal
exit /b 0
