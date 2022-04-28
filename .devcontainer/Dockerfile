FROM paperist/texlive-ja:debian

ARG USERNAME
ARG UID
ARG GID

ENV PYTHON_VERSION="3.9.5"
ENV PYENV_ROOT="/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/pyenv/pyenv.git ${PYENV_ROOT} \
    && pyenv install ${PYTHON_VERSION} \
    && pyenv global ${PYTHON_VERSION} \
    && pyenv rehash \
    && chmod -R 777 /.pyenv

RUN useradd -u $UID -o -m $USERNAME
RUN groupmod -g $GID -o $USERNAME
