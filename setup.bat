venv\Scripts\pip3 install -r requirements.txt
echo user = %userprofile%>> .env
echo start %~dp0venv\Scripts\pythonw %~dp0main.pyw> watcher.bat
move "watcher.bat" "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup"
