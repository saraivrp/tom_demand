@echo off
echo ========================================
echo Building TOM Demand for Windows
echo ========================================
echo.

REM Create virtual environment
if not exist "venv_win" (
    echo Creating virtual environment...
    python -m venv venv_win
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Please make sure Python is installed and in PATH
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv_win\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Install PyInstaller
echo Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

REM Build executable
echo.
echo Building Windows executable...
pyinstaller --onefile --name=tom_demand --add-data "config;config" --add-data "src;src" --hidden-import=click --hidden-import=pandas --hidden-import=numpy --hidden-import=yaml --hidden-import=colorama --hidden-import=tqdm tom_demand.py
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESS!
echo ========================================
echo Executable location: dist\tom_demand.exe
echo Size: 
dir dist\tom_demand.exe | find "tom_demand.exe"
echo.
echo To test: dist\tom_demand.exe --help
echo.
pause
