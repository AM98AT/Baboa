@echo off
REM ===== Publishes your latest data.json to the online website =====
cd /d "%~dp0"

echo Saving and uploading the new test results...
git add data.json
git commit -m "Update test results"
git push

echo.
echo ============================================================
echo  Done! The website will show the new results in ~1 minute.
echo ============================================================
pause
