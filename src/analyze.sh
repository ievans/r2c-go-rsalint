#!/bin/bash

set -e
CODE_DIR="/analysis/inputs/public/source-code"

cd ${CODE_DIR}
export GOPATH=/home/go
export GOBIN=$GOPATH/bin
mkdir -p /home/go/input
mkdir -p /home/go/bin
cp -r ${CODE_DIR} /home/go/input

cd /home/go/input/source-code

go get ./...

rsalint --json . | python3 /analyzer/formatter.py /home/go/input/source-code >/analysis/output/output.json
