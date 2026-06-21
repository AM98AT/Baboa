@echo off
REM ===== Opens the drag-and-drop tool to add new lab results into results.json =====
cd /d "%~dp0"
set PYTHONUTF8=1
echo Opening the "Add new results" tool in your browser...
streamlit run merge_ui.py --server.port=8502
pause
