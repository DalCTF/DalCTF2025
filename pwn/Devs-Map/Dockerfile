FROM ubuntu:24.04

RUN apt-get update && apt-get -y install xinetd lib32z1  

RUN useradd -u 1337 -m ctf

WORKDIR /ctf

COPY xinetd.conf ./
COPY flag.txt ./
COPY challenge.sh ./
COPY devs_map ./


CMD ["xinetd", "-dontfork", "-f", "xinetd.conf"]
