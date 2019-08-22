FROM continuumio/miniconda3

RUN apt-get -qq update --yes \
 && apt-get -qq install --yes --no-install-recommends \
    build-essential git make clang libboost-dev postgresql-client ca-certificates \
 && rm -rf /var/lib/apt/lists/*

ARG PYTHON
ADD ci/requirements-$PYTHON-dev.yml /

RUN export CONDA_BIN=/opt/conda/bin/conda \
  && $CONDA_BIN config --add channels conda-forge \
  && $CONDA_BIN update --all --yes --quiet \
  && $CONDA_BIN env create --name ibis-env --file /requirements-$PYTHON-dev.yml \
  && $CONDA_BIN install --yes conda-build \
  && $CONDA_BIN install -n ibis-env --yes openjdk=8 \
  && $CONDA_BIN clean --all --yes

RUN echo 'source activate ibis-env && exec "$@"' > activate.sh

COPY . /ibis
WORKDIR /ibis

RUN bash /activate.sh pip install -e . --no-deps --ignore-installed --no-cache-dir

ENTRYPOINT ["bash", "/activate.sh"]
