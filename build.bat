@echo off
setlocal
cd /d "%~dp0"

echo Installing dependencies...
pip install yt-dlp pyinstaller --quiet

echo Building exe...
pyinstaller --onefile --windowed --icon=app_icon.ico --name "YT Playlist Extractor" yt_playlist_extractor.py

echo Creating desktop shortcut...
powershell -NoProfile -Command ^
  "$s=(New-Object -COM WScript.Shell).CreateShortcut(\"$env:USERPROFILE\Desktop\YT Playlist Extractor.lnk\"); $s.TargetPath=\"%cd%\dist\YT Playlist Extractor.exe\"; $s.IconLocation=\"%cd%\app_icon.ico\"; $s.WorkingDirectory=\"%cd%\dist\"; $s.Save()"

echo Done. Shortcut placed on Desktop.
pause
