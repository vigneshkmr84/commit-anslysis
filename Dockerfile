FROM python:3.9-alpine AS builder

RUN apk add --no-cache git
RUN git --version


#COPY ./requirements.txt /tmp/
COPY ./git-repo-pull.py /tmp/
COPY ./config/repo.config /tmp/config/

#RUN pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /tmp/

RUN python git-repo-pull.py

FROM mongo

COPY ./index.js /tmp
COPY --from=builder /tmp/commit-data/output/consolidated-output.json /tmp 
CMD mongoimport --host mongodb --db commit-analysis --collection commits_data --type json --file /tmp/consolidated-output.json --jsonArray

CMD mongosh mongodb://mongodb/commit-analysis < /tmp/index.js

