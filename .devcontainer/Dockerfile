FROM python:3.11-bullseye

ENV PYTHONPATH=.
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PIP_INDEX_URL=https://repo.int.saarstahl.de/repository/pypi-all/simple
ENV PIP_TRUSTED_HOST="nexus.int.shsservices.de repo.int.saarstahl.de"

# Add non-root user
ARG USERNAME=nonroot
RUN groupadd --gid 1000 $USERNAME && useradd --uid 1000 --gid 1000 -m $USERNAME
## Make sure to reflect new user in PATH
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
RUN ln -s bash /bin/sh.bash && mv /bin/sh.bash /bin/sh
USER $USERNAME

## Pip dependencies
RUN pip install --upgrade pip
# Install development dependencies
COPY --chown=nonroot:1000 requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt && rm /tmp/requirements-dev.txt
# Install production dependencies
COPY --chown=nonroot:1000 requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

ENTRYPOINT ["/bin/bash"]