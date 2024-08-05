where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installe Python 3.12.
    exit /b 1
)

pip install requests
pip install pygame
pip install astral
pip install schedule
pip install pillow
