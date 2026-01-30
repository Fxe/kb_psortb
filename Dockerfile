FROM brinkmanlab/psortb_commandline:1.0.2
LABEL maintainer="fliu@anl.gov"

ENV TZ=Etc/UTC
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_PROGRESS_BAR=off

# -----------------------------------------
# Install system dependencies
# -----------------------------------------
RUN apt-get update
RUN apt-get install -y build-essential \
                       git \
                       unzip \
                       htop \
                       curl \
                       gcc
RUN apt-get install -y openjdk-9-jre-headless
#RUN rm -rf /var/lib/apt/lists/*

# Copy in the SDK
COPY --from=kbase/kb-sdk:1.2.1 /src /sdk
RUN sed -i 's|/src|/sdk|g' /sdk/bin/*
ENV PATH=/sdk/bin:$PATH

ADD biokbase /opt/conda/lib/python3.11/site-packages
ADD biokbase/user-env.sh /kb/deployment/user-env.sh

# Install uv (goes to /root/.local/bin by default)
RUN wget -qO- https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"
ENV UV_PYTHON_INSTALL_DIR=/opt/uv-python
# Install Python 3.10 and make a venv that becomes the default python
RUN uv python install 3.10
RUN uv venv /opt/venv --python 3.10
# Make that venv the default interpreter for subsequent RUN/CMD/ENTRYPOINT
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

ADD requirements_kbase.txt /tmp/requirements_kbase.txt
RUN uv pip install -r /tmp/requirements_kbase.txt

# -----------------------------------------
# add a modified version that allows outputfile specification
COPY ./psortx /usr/local/psortb/bin/psortx

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
