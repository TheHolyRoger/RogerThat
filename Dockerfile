# Set the base image
FROM ubuntu:20.04 AS builder

# Install linux dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y gcc \
        build-essential pkg-config libusb-1.0 curl git libpq-dev \
        sudo && \
    rm -rf /var/lib/apt/lists/*

# Add rogerthat user
RUN useradd -m -s /bin/bash rogerthat

# Switch to rogerthat user
USER rogerthat:rogerthat
WORKDIR /home/rogerthat

# Install miniconda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-py38_4.8.2-Linux-x86_64.sh -o ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b && \
    rm ~/miniconda.sh && \
    ~/miniconda3/bin/conda update -n base conda -y && \
    ~/miniconda3/bin/conda clean -tipsy

# Dropping default ~/.bashrc because it will return if not running as interactive shell, thus not invoking PATH settings
RUN :> ~/.bashrc

# Copy environment only to optimize build caching, so changes in sources will not cause conda env invalidation
COPY --chown=rogerthat:rogerthat support/environment.yml .

# ./install | create rogerthat environment
RUN ~/miniconda3/bin/conda env create -f environment.yml && \
    ~/miniconda3/bin/conda clean -tipsy && \
    # clear pip cache
    rm -rf /home/rogerthat/.cache

# Copy remaining files
COPY --chown=rogerthat:rogerthat alembic/ alembic/
COPY --chown=rogerthat:rogerthat bin/ bin/
COPY --chown=rogerthat:rogerthat rogerthat/ rogerthat/
COPY --chown=rogerthat:rogerthat scripts/ scripts/
COPY --chown=rogerthat:rogerthat tests/ tests/
COPY --chown=rogerthat:rogerthat alembic.ini .
COPY --chown=rogerthat:rogerthat support/docker_compose_entrypoint.sh .
COPY --chown=rogerthat:rogerthat support/docker_start_python.sh .
COPY --chown=rogerthat:rogerthat support/docker_start_setup_script.sh .
COPY --chown=rogerthat:rogerthat support/generate_self_signed_cert.sh .
COPY --chown=rogerthat:rogerthat support/wait-for-it.sh .
COPY --chown=rogerthat:rogerthat LICENSE .
COPY --chown=rogerthat:rogerthat README.md .

# activate rogerthat env when entering the CT
RUN echo "source /home/rogerthat/miniconda3/etc/profile.d/conda.sh && conda activate $(head -1 environment.yml | cut -d' ' -f2)" >> ~/.bashrc

# Build final image using artifacts from builer
FROM ubuntu:20.04 AS release
# Dockerfile author / maintainer 
LABEL maintainer="TheHoliestRoger <theholyroger@theholyroger.com>"

# Build arguments
ARG BRANCH=""
ARG COMMIT=""
ARG BUILD_DATE=""
LABEL branch=${BRANCH}
LABEL commit=${COMMIT}
LABEL date=${BUILD_DATE}

# Set ENV variables
ENV COMMIT_SHA=${COMMIT}
ENV COMMIT_BRANCH=${BRANCH}
ENV BUILD_DATE=${DATE}

ENV STRATEGY=${STRATEGY}
ENV CONFIG_FILE_NAME=${CONFIG_FILE_NAME}
ENV WALLET=${WALLET}
ENV CONFIG_PASSWORD=${CONFIG_PASSWORD}

ENV INSTALLATION_TYPE=docker

# Add rogerthat user
RUN useradd -m -s /bin/bash rogerthat && \
  ln -s /configs /home/rogerthat/configs && \
  ln -s /logs /home/rogerthat/logs && \
  ln -s /data /home/rogerthat/data

# Create mount points
RUN mkdir /configs /logs /data /certs && chown -R rogerthat:rogerthat /configs /logs /data /certs
VOLUME /configs /logs /data /certs

# Install packages required in runtime
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y sudo libusb-1.0 openssl && \
    rm -rf /var/lib/apt/lists/*

# Switch to rogerthat user
USER rogerthat:rogerthat
WORKDIR /home/rogerthat

# Copy all build artifacts from builder image
COPY --from=builder --chown=rogerthat:rogerthat /home/ /home/

# additional configs (sudo)
COPY support/docker/etc /etc

# Setting bash as default shell because we have .bashrc with customized PATH (setting SHELL affects RUN, CMD and ENTRYPOINT, but not manual commands e.g. `docker run image COMMAND`!)
SHELL [ "/bin/bash", "-lc" ]
RUN python scripts/setup.py -s
CMD python bin/start_rogerthat.py
