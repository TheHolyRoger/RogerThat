@echo off

@SET SCRIPT=%~nx0
@SET FNAME=%~f0
@SET nostart=0
@SET dontbuild=0
@SET dockerprune=0

:GETOPTS
    if /I "%1" == "-h" GOTO Help
    if /I "%1" == "-n" SET nostart=1 & SHIFT
    if /I "%1" == "-d" SET dontbuild=1 & SHIFT
    if /I "%1" == "-p" SET dockerprune=1 & SHIFT
    SHIFT
if not "%1" == "" GOTO Help

if %dockerprune% == 1 (ECHO Pruning docker. && docker system prune -f)

if %dontbuild% == 1 (ECHO Skipping build.) else (docker image prune -f && docker build -t rogerthat:latest .)

REM Run setup script via docker
CALL scripts\start_docker_setup_script.bat -s

if %nostart% == 1 ( ECHO Skipping start.) else (docker compose up)

EXIT /B 0

:Help
ECHO.
ECHO Help documentation for %SCRIPT%
ECHO.
ECHO Usage: %FNAME% [ -n ] [ -d ] [ -p ]
ECHO.
ECHO Use the following optional switches.
ECHO.
ECHO -n  --Skip starting.
ECHO -d  --Don't Build.
ECHO -p  --Prune docker.
GOTO:EOF
