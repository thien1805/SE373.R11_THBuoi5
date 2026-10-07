@echo off
cd /d "%~dp0"
set "GIT_PATH=C:\Program Files\Microsoft SQL Server Management Studio 21\Release\Common7\IDE\CommonExtensions\Microsoft\TeamFoundation\Team Explorer\Git\cmd\git.exe"
echo ========================================================
echo   DANG PUSH MA NGUON LEN GITHUB (SE373.R11_THBuoi5)
echo ========================================================
"%GIT_PATH%" push -u origin main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Phat hien xung dot nhanh hoac chua co force. Dang thu push force...
    "%GIT_PATH%" push -u origin main --force
)
echo.
pause
