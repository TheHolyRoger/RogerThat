@echo off

for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set ParentFolderName=%%~dpnxJ
cd  %ParentFolderName%

docker-compose run --rm --entrypoint "/bin/sh /generate_self_signed_cert.sh" certbot
