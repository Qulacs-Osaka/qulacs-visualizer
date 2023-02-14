FROM paperist/texlive-ja:debian

ARG USERNAME
ARG UID
ARG GID

ENV PYTHON_VERSION="3.9.13"
ENV PYENV_ROOT="/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"
ENV USE_LATEX=yes

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    git \
    gpg \
    poppler-utils \
    gosu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# gosu is used instead of sudo in postStartCommand of devcontainer.json.
# This command allows a non-root user to run as the root user using gosu.
# ref: https://github.com/tianon/gosu/issues/11
RUN chmod +s /usr/sbin/gosu

RUN git clone https://github.com/pyenv/pyenv.git ${PYENV_ROOT} \
    && pyenv install ${PYTHON_VERSION} \
    && pyenv global ${PYTHON_VERSION} \
    && pyenv rehash \
    && chmod -R 777 /.pyenv

RUN useradd -u $UID -o -m $USERNAME
RUN groupmod -g $GID -o $USERNAME

# Requires $POETRY_HOME to install the location; poetry is installed under /root by default.
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/home/${USERNAME}/.local python3 -
