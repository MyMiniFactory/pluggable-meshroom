FROM nvidia/cuda:10.1-base-ubuntu18.04

ARG UNAME=worker
ARG UID=1000
ARG GID=1000

WORKDIR /app

RUN apt-get update \
    && apt-get install -y python3.6 wget unzip \
    && groupadd --gid $GID $UNAME \
    && useradd --gid $GID --uid $UID $UNAME \
    && wget https://github.com/MyMiniFactory/plugable-meshroom/releases/download/2018.1.0/Meshroom-2018.1.0.zip \
    && unzip /app/Meshroom-2018.1.0.zip

COPY python_wrapper /app/python_wrapper/

RUN chown -R $UNAME:$UNAME /app && chmod u+x /app/Meshroom-2018.1.0/aliceVision/bin/*

USER $UNAME

ENTRYPOINT ["python3.6","/app/python_wrapper/process.py"]
