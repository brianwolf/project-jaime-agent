# COMPILER
# ---------------------------------------------
FROM python:3.9-slim as compiler

WORKDIR /home/jaime
COPY . . 

RUN useradd -m -d /home/jaime jaime
RUN chmod 777 -R .
USER jaime

RUN pip install compile

RUN python -m compile -b -f -o dist/ .
RUN rm -fr dist/repo_modules_default

# EXECUTION
# ---------------------------------------------
FROM python:3.9-slim

WORKDIR /home/jaime
ENV HOME=/home/jaime

RUN apt-get update
RUN apt-get install iputils-ping curl git wget -y

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN rm -fr requirements.txt

COPY --from=compiler /home/jaime/dist/ ./
COPY logic/resources logic/resources

RUN useradd -m -d /home/jaime jaime
RUN chmod 777 -R .
USER jaime

COPY --from=compiler /home/jaime/dist/ ./
COPY logic/resources logic/resources

ARG ARG_VERSION=local

ENV VERSION=${ARG_VERSION}
ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=7001
ENV AGENT_TYPE=BASE
ENV WORKINGDIR_PATH=/data/workingdir
ENV TZ America/Argentina/Buenos_Aires

ENV EXTRA_CMD="cd ."
CMD ${EXTRA_CMD} & python3 -m gunicorn -b ${PYTHON_HOST}:${PYTHON_PORT} --workers=1 --threads=4 app:app

EXPOSE 7001