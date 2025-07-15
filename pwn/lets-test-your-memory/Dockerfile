FROM ubuntu:24.04

RUN apt-get update && apt-get -y install xinetd lib32z1 gdb gcc

RUN useradd -m ctf

WORKDIR /ctf

COPY xinetd.conf ./
COPY flag.txt ./
COPY challenge.sh ./
COPY lets-test-your-memory ./
COPY main.c ./


CMD ["xinetd", "-dontfork", "-f", "xinetd.conf"]
