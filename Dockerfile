# COMPILER
# ---------------------------------------------
FROM python:3.10-slim as compiler

USER root

WORKDIR /home/jaime

RUN pip install compile

COPY logic/ logic/
COPY app.py app.py

RUN python -m compile -b -f -o dist/ .
RUN rm -fr dist/repo_modules_default

# EXECUTION
# ---------------------------------------------
FROM python:3.10-slim

USER root

RUN apt-get update
RUN apt-get install iputils-ping curl git wget procps -y

WORKDIR /home/jaime
ENV HOME=/home

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN rm -fr requirements.txt

RUN useradd -ms /bin/bash -d /home/jaime 1001
RUN chmod 777 -R /home
USER 1001

COPY --from=compiler /home/jaime/dist/ ./
COPY logic/resources logic/resources

ARG ARG_VERSION=local

ENV VERSION=${ARG_VERSION}
ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=7001
ENV AGENT_TYPE=BASE
ENV WORKINGDIR_PATH=.shared/workingdir/
ENV TZ=America/Argentina/Buenos_Aires

ENV EXTRA_CMD="cd ."
CMD ${EXTRA_CMD} & python3 -m gunicorn -b ${PYTHON_HOST}:${PYTHON_PORT} --workers=1 --threads=4 app:app

EXPOSE 7001