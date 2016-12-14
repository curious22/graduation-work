FROM ubuntu:14.04

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y build-essential libssl-dev libffi-dev python-dev && \
    apt-get install -y python3-dev python3-pip libxml2-dev libxslt1-dev

COPY requirements.txt /src/requirements.txt

RUN pip3 install -r /src/requirements.txt

CMD ["/bin/bash"]