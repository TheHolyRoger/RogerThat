@echo off
docker run -it --rm  --volume "%cd%/configs:/configs" rogerthat:latest ./start_docker_setup_script.sh %*
