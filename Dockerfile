FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y dialog && \
    apt-get install -y apt-utils && \
    apt-get upgrade -y && \
    apt-get install -y gcc && \
    apt-get install -y sudo

# This adds the `default` user in to sudoers with full privileges:
RUN HOME=/home/default && \
    mkdir -p ${HOME} && \
    GROUP_ID=1000 && \
    USER_ID=1000 && \
    groupadd -r default -f -g "$GROUP_ID" && \
    useradd -u "$USER_ID" -r -g default -d "$HOME" -s /sbin/nologin \
        -c "Default Application User" default && \
    chown -R "$USER_ID:$GROUP_ID" ${HOME} && \
    usermod -a -G sudo default && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN apt-get install -y vim && \
    apt-get install -y make && \
    apt-get install -y cmake && \
    apt-get install -y git && \
    apt-get install -y libssl-dev && \
    apt-get install -y python3 && \
    apt-get install -y python-pip && \
    apt-get install -y python3-pip && \
    python -m pip install --upgrade pip && \
    python -m pip install --upgrade cldoc && \
    python -m pip install jupyter 
 
WORKDIR /home/default

RUN apt-get install wget -y
RUN apt-get install graphviz -y
RUN apt-get install -f -y

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN pip3 install pipenv

USER default

WORKDIR /build
CMD ["/bin/bash"]
