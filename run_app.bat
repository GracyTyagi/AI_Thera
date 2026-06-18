@echo off
TITLE AI Thera Launcher
echo -----------------------------------------
echo 🌿 AI Thera: Mental Wellness Platform
echo -----------------------------------------
echo.
echo Checking dependencies... Please wait.
echo.

:: Navigate to the project directory
cd /d "C:\Users\gracy\OneDrive\Desktop\AI_Thera"

:: Ensure all requirements are installed
python -m pip install -r requirements.txt --quiet

echo.
echo Starting the application...
echo.

:: Run the streamlit app using 'python -m streamlit' with auto-reload enabled
python -m streamlit run app.py --server.runOnSave true

:: Keep the window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Something went wrong while starting the app.
    echo Please make sure Python is installed and added to PATH.
    pause
)
