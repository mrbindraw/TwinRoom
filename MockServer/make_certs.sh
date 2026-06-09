#!/usr/bin/env bash

set -e
mkdir -p certs
cd certs

echo "==> 1/4  Private key CA"
openssl genrsa -out ca.key 2048

echo "==> 2/4  Root certificate CA (10 years)"
openssl req -new -x509 -days 3650 -key ca.key -out ca.crt -subj "/CN=TwinRoom"

echo "==> 3/4  Private key + request for broker (CN=localhost)"
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -subj "/CN=localhost"

echo "==> 4/4  Sign broker certificate our CA (10 years)"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 3650

echo "Done!"
