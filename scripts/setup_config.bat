@echo off

for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set ParentFolderName=%%~dpnxJ
cd  %ParentFolderName%

docker run -it --rm  --volume "%cd%/configs:/configs" theholiestroger/rogerthat:latest ./docker_start_setup_script.sh %*
