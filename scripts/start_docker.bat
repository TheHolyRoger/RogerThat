@echo off

for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set ParentFolderName=%%~dpnxJ
cd  %ParentFolderName%


@SET SCRIPT=%~nx0
@SET FNAME=%~f0
@SET daemon=""
@SET withcertbot=""
@SET dockerprune=0

:GETOPTS
    if /I "%1" == "-h" GOTO Help
    if /I "%1" == "-d" SET daemon="-d" & SHIFT
    if /I "%1" == "-c" SET withcertbot="certbot" & SHIFT
    if /I "%1" == "-p" SET dockerprune=1 & SHIFT
    SHIFT
if not "%1" == "" GOTO Help

if %dockerprune% == 1 (ECHO Pruning docker. && docker system prune -f)

REM Run setup script via docker
CALL scripts\setup_config.bat -s

docker-compose up %daemon% db rogerthat nginx %withcertbot%
if not "%daemon%" == "" (scripts\setup_config.bat  --print-splash)

EXIT /B 0

:Help
ECHO.
ECHO Help documentation for %SCRIPT%
ECHO.
ECHO Usage: %FNAME% [ -p ] [ -d ]
ECHO.
ECHO Use the following optional switches.
ECHO.
ECHO -p  --Prune docker.
ECHO -d  --Run as daemon.
ECHO -c  --Run with certbot renewing every 6 hours (Requires certificate to be set-up).
GOTO:EOF
