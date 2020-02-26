FROM golang:1.13.8-buster

RUN apt-get update \
  && apt-get install -y python3 python3-pip python3-setuptools \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# TODO: Analyzer specific packages below

# Setup analysis user for docker
RUN groupadd -r analysis && useradd -m --no-log-init --gid analysis analysis
USER root
COPY src /analyzer

RUN go get -u -v github.com/picatz/rsalint/cmd/...
#RUN rsalint --help


# Setup entrypoint into the analysis code logic
WORKDIR /
CMD ["/analyzer/analyze.sh"]