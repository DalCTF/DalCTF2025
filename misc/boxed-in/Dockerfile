FROM ubuntu:24.04

RUN apt-get update && apt-get -y install xinetd lib32z1 python3

RUN useradd -m ctf

WORKDIR /ctf

COPY xinetd.conf ./
COPY flag.txt ./
COPY challenge.sh ./
COPY main.py ./


CMD ["xinetd", "-dontfork", "-f", "xinetd.conf"]
