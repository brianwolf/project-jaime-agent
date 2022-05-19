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
ENV PYTHON_PORT=7001
ENV AGENT_TYPE=OPENSHIFT
ENV RUN_ON_DOCKER=true
ENV WORKINGDIR_PATH=/data/workingdir

ENV TZ America/Argentina/Buenos_Aires

RUN apt-get update
RUN apt-get install iputils-ping curl git wget -y

RUN wget -O oc.tar.gz "https://access.cdn.redhat.com/content/origin/files/sha256/16/161b747294f9877d1e028fd88bda4469d2834441c3052a36415e7f9e2c9340d6/oc-4.10.14-linux.tar.gz?user=f169512860a6b13655881f317b35e2f8&_auth_=1652991271_2887dc5b35d29c53cd7e715e5b05241f"
RUN tar -xf oc.tar.gz -C /usr/local/bin/
RUN rm oc.tar.gz

CMD gunicorn \
    -b ${PYTHON_HOST}:${PYTHON_PORT} \
    --workers=1 \
    --threads=4 \
    app:app

COPY requirements.txt ./
RUN pip install -r requirements.txt --upgrade pip
RUN rm -fr requirements.txt

COPY --from=compiler /home/src/dist/ ./
COPY logic/resources logic/resources