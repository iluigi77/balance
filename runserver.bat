@echo off
cmd /k "cd /d C:\users\ninaka\use\lambu\opt\venv\Scripts & activate & cd /d C:\Users\ninaka\use\lambu\dev\client\balance-project & waitress-serve --port=5000 wsgi:application"
REM cmd /k "cd /d C:\users\ninaka\use\lambu\opt\venv\Scripts & activate & cd /d C:\Users\ninaka\use\lambu\dev\client\balance-project & flask run"
