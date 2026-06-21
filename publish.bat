@echo off
REM ===== Publishes your latest results to the online website =====
cd /d "%~dp0"

REM Rebuild the Arabic info file (instant; safe to run every time).
set PYTHONUTF8=1
python build_ar.py

echo.
echo Saving and uploading the new test results...
git add results.json info.json info_en.json
git commit -m "Update test results"
git push

echo.
echo ============================================================
echo  Done! The website will show the new results in ~1 minute.
echo ============================================================
pause
