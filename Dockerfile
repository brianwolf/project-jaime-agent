# COMPILER
# ---------------------------------------------
FROM python:3.9-slim as compiler

WORKDIR /home/src
COPY . .

RUN pip install compile --upgrade pip

RUN python -m compile -b -f -o dist/ .
RUN rm -fr dist/repo_modules_default

# EXECUTION
# ---------------------------------------------
FROM python:3.9-slim

WORKDIR /home/jaime-agent
ENV HOME=/home/jaime-agent

RUN apt-get update
RUN apt-get install iputils-ping curl git wget -y

COPY requirements.txt ./
RUN pip install -r requirements.txt --upgrade pip
RUN rm -fr requirements.txt

RUN useradd -m -d /home/jaime-agent jaime-agent
RUN chmod 777 . -R
USER jaime-agent

ARG ARG_VERSION=local

ENV VERSION=${ARG_VERSION}
ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=7001
ENV AGENT_TYPE=BASE
ENV WORKINGDIR_PATH=/data/workingdir
ENV TZ America/Argentina/Buenos_Aires

ENV EXTRA_CMD="cd ."
CMD ${EXTRA_CMD} & python3 -m gunicorn -b ${PYTHON_HOST}:${PYTHON_PORT} --workers=1 --threads=4 app:app

COPY --from=compiler /home/src/dist/ ./
COPY logic/resources logic/resources

EXPOSE 7001