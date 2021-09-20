@echo off
docker run -it --rm  --volume "%cd%/certs:/certs" theholiestroger/rogerthat:latest scripts/generate_self_signed_cert.sh
