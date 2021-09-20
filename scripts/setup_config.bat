@echo off
docker run -it --rm  --volume "%cd%/configs:/configs" theholiestroger/rogerthat:latest ./docker_start_setup_script.sh %*
