@echo off

for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set ParentFolderName=%%~dpnxJ
for %%a in ("%ParentFolderName%") do set "ParentFolderName=%%~dpa"
cd  %ParentFolderName%


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

if %dontbuild% == 1 (ECHO Skipping build.) else (docker image prune -f && docker compose build)

REM Run setup script via docker
CALL scripts\setup_config.bat -s

if %nostart% == 1 ( ECHO Skipping start.) else (docker compose up db rogerthat nginx)

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
