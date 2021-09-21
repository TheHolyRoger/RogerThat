@ECHO OFF
@SET ENV_FILE=support\environment.yml
IF EXIST "C:\ProgramData\Miniconda3\Scripts\activate.bat" goto activate_miniconda
IF EXIST "C:\ProgramData\Anaconda3\Scripts\activate.bat" goto activate_anaconda

echo Couldnt find Miniconda or Anaconda, exiting.
exit /b 0

:activate_miniconda
call C:\ProgramData\Miniconda3\Scripts\activate.bat C:\ProgramData\Miniconda3
goto update_environment

:activate_anaconda
call C:\ProgramData\Anaconda3\Scripts\activate.bat C:\ProgramData\Anaconda3
goto update_environment

:update_environment
setlocal EnableDelayedExpansion
SET lf=-
FOR /F "delims=" %%i IN ('conda env list ^| findstr "rogerthat"') DO if ("!ENV_FOUND!"=="") (set ENV_FOUND=%%i) else (set ENV_FOUND=!ENV_FOUND!%lf%%%i)
echo %ENV_FOUND%
if "%ENV_FOUND%" == "" (conda env create -f %ENV_FILE% && echo Created environment.) else (conda env update -f %ENV_FILE% && echo Updated environment.)
call activate rogerthat
