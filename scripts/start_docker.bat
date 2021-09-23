@echo off

for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set ParentFolderName=%%~dpnxJ
cd  %ParentFolderName%


@SET SCRIPT=%~nx0
@SET FNAME=%~f0
@SET dockerprune=0

:GETOPTS
    if /I "%1" == "-h" GOTO Help
    if /I "%1" == "-p" SET dockerprune=1 & SHIFT
    SHIFT
if not "%1" == "" GOTO Help

if %dockerprune% == 1 (ECHO Pruning docker. && docker system prune -f)

REM Run setup script via docker
CALL scripts\setup_config.bat -s

docker compose up

EXIT /B 0

:Help
ECHO.
ECHO Help documentation for %SCRIPT%
ECHO.
ECHO Usage: %FNAME% [ -p ]
ECHO.
ECHO Use the following optional switches.
ECHO.
ECHO -p  --Prune docker.
GOTO:EOF
