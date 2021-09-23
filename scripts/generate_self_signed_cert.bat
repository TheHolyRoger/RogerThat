@echo off

for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set ParentFolderName=%%~dpnxJ
cd  %ParentFolderName%

docker run -it --rm  --volume "%cd%/certs:/certs" theholiestroger/rogerthat:latest ./generate_self_signed_cert.sh
