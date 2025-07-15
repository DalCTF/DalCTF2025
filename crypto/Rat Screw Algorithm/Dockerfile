FROM ubuntu:24.04

RUN apt-get update && apt-get -y install xinetd lib32z1 python3 pip
RUN pip install --no-cache-dir pycryptodome --break-system-packages

RUN useradd -m ctf

WORKDIR /ctf

COPY xinetd.conf ./
COPY challenge.sh ./
COPY main.py ./


CMD ["xinetd", "-dontfork", "-f", "xinetd.conf"]
