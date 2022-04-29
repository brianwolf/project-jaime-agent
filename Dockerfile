# COMPILER
# ---------------------------------------------
FROM python:3.9-slim as compiler

WORKDIR /home/src
COPY . .

RUN pip install compile --upgrade pip

RUN	python -m compile -b -f -o dist/ .
RUN rm -fr dist/repo_modules_default


# EXECUTION
# ---------------------------------------------
FROM python:3.9-slim

WORKDIR /home/src

ARG ARG_VERSION=local

ENV VERSION=${ARG_VERSION}
ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=80
ENV AGENT_TYPE=OPENSHIFT
ENV RUN_ON_DOCKER=true
ENV WORKINGDIR_PATH=/data/workingdir

ENV TZ America/Argentina/Buenos_Aires

ADD resources/oc.tar.gz /usr/local/bin/
RUN rm -fr resources

RUN apt-get update
RUN apt-get install iputils-ping curl git -y

CMD gunicorn \
    -b ${PYTHON_HOST}:${PYTHON_PORT} \
    --workers=1 \
    --threads=4 \
    app:app

COPY requirements.txt ./
RUN pip install -r requirements.txt --upgrade pip
RUN rm -fr requirements.txt

COPY --from=compiler /home/src/dist/ ./
