@echo off
echo Forcing Claude logout by clearing session data...

:: Clear Chrome cookies and session data for Claude
echo Clearing Chrome data...
taskkill /F /IM chrome.exe 2>nul
timeout /t 2 /nobreak >nul
rd /s /q "%LocalAppData%\Google\Chrome\User Data\Default\Sessions" 2>nul
rd /s /q "%LocalAppData%\Google\Chrome\User Data\Default\Session Storage" 2>nul
del "%LocalAppData%\Google\Chrome\User Data\Default\Cookies" 2>nul
del "%LocalAppData%\Google\Chrome\User Data\Default\Preferences" 2>nul

:: Clear Edge cookies and session data for Claude
echo Clearing Edge data...
taskkill /F /IM msedge.exe 2>nul
timeout /t 2 /nobreak >nul
rd /s /q "%LocalAppData%\Microsoft\Edge\User Data\Default\Sessions" 2>nul
rd /s /q "%LocalAppData%\Microsoft\Edge\User Data\Default\Session Storage" 2>nul
del "%LocalAppData%\Microsoft\Edge\User Data\Default\Cookies" 2>nul

:: Clear Firefox session data
echo Clearing Firefox data...
taskkill /F /IM firefox.exe 2>nul
timeout /t 2 /nobreak >nul
for /d %%i in ("%AppData%\Mozilla\Firefox\Profiles\*") do (
    del "%%i\cookies.sqlite" 2>nul
    del "%%i\sessionstore.jsonlz4" 2>nul
    del "%%i\sessionstore-backups\*" 2>nul
)

:: Clear DNS cache
echo Clearing DNS cache...
ipconfig /flushdns >nul

echo.
echo Claude logout complete! All browsers have been closed and session data cleared.
echo You can now login with a different account.
echo.
pause