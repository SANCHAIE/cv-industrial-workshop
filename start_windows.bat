@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
where uv >nul 2>nul
if errorlevel 1 (
  echo กำลังติดตั้ง uv ^(ตัวจัดการ Python^) ครั้งเดียว...
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  set "PATH=%USERPROFILE%\.local\bin;%PATH%"
)
echo กำลังเตรียม Python 3.12 และไลบรารีทั้งหมด ^(ครั้งแรกใช้เวลา 2-5 นาที^)...
uv sync
if errorlevel 1 (
  echo ติดตั้งไม่สำเร็จ ถ่ายภาพหน้าจอนี้ส่งให้ TA
  pause
  exit /b 1
)
echo.
echo เลือก:  1 = ตรวจความพร้อม   2 = เปิด Notebook   3 = เปิด Web app
set /p c="พิมพ์ตัวเลขแล้วกด Enter: "
if "%c%"=="1" ( uv run check_setup.py & pause ) else if "%c%"=="3" ( uv run streamlit run app/inspection_app.py ) else ( uv run jupyter lab notebooks )
