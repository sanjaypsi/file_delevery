set APPDIR=%~dp0
set PYTHONEXE=%APPDIR%\python\python37\Scripts\python.exe
set PYTHONPATH=%PYTHONPATH=%;%APPDIR%\packages;%APPDIR%\source
set SCRIPT=%APPDIR%\source\file_delivery\main.py


%PYTHONEXE% %SCRIPT%
pause
