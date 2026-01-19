@echo off
echo ========================================
echo     The PDFinator - Installation
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    echo.
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
echo.

echo Installing PyPDF2...
pip install pypdf2

echo Installing PyMuPDF...
pip install PyMuPDF

echo Installing pycryptodome...
pip install pycryptodome

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo You can now run The PDFinator with:
echo     python PDFinator.py
echo.
echo Place your PDF files in the 'pdfs' folder
echo and use the GUI to process them.
echo.
pause