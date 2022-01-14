FROM python:3.9-slim-bullseye AS builder

RUN apt update && apt install git -y && apt-get -yq install ssh
RUN git --version

COPY ./requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

#COPY ./config/repo.config /tmp/config/
COPY ./config/ /tmp/config/

COPY ./git-repo-pull.py /tmp/
COPY ./parser.py /tmp/


WORKDIR /tmp/
USER root
RUN whoami


RUN mkdir -p /root/.ssh/ \ 
    && chmod 777 /root/.ssh/ \
    && touch /root/.ssh/id_rsa \
    && touch /root/.ssh/known_hosts \
    && chmod 600 /root/.ssh/known_hosts \
    && chmod 600 /root/.ssh/id_rsa \
    && ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN ssh-keyscan github.com

RUN python parser.py
RUN python git-repo-pull.py

FROM mongo

COPY --from=builder /tmp/commit-data/output/consolidated-output.csv /tmp 
COPY ./index.js /tmp
COPY ./entrypoint.sh /tmp

CMD ["bash", "/tmp/entrypoint.sh"]

