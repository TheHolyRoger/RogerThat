@echo off

for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set ParentFolderName=%%~dpnxJ
cd  %ParentFolderName%

echo ### Begin generating certificate

CALL scripts\setup_config.bat -s

docker-compose stop

echo ### Downloading SSL params ...
docker-compose run --rm --entrypoint "/bin/sh /letsencrypt_download_params.sh" certbot


echo ### Starting nginx ...
docker-compose up --force-recreate -d nginx
echo.


echo ### Requesting Let's Encrypt certificate ...
docker-compose run --rm --entrypoint "/bin/sh /letsencrypt_generate.sh" certbot

echo ### Stopping nginx ...
docker-compose stop nginx

echo ### Finished generating certificate you can now start RogerThat!
