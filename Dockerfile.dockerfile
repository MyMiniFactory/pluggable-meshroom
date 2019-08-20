FROM nvidia/cuda:10.1-base-ubuntu18.04

ARG UNAME=worker
ARG UID=1000
ARG GID=1000

RUN apt-get update \
    && apt-get install -y python3.6 \
    && groupadd --gid $GID $UNAME \
    && useradd --gid $GID --uid $UID $UNAME

WORKDIR /app

COPY python_wrapper /app/python_wrapper/
COPY Meshroom-2018.1.0 /app/Meshroom-2018.1.0/

RUN chown -R $UNAME:$UNAME /app && chmod u+x /app/Meshroom-2018.1.0/aliceVision/bin/*

USER $UNAME

ENTRYPOINT ["python3.6","/app/python_wrapper/process.py"]
