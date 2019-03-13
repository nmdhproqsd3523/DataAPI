#!/bin/bash

mkdir -p ./CA/{private,newcerts}
touch ./CA/index.txt 
touch ./CA/serial
echo 01 > ./CA/serial

# ca
openssl genrsa -out ca.key 2048
# 证书申请+自签名
openssl req -key ca.key -new -x509 -days 7500 -sha256 -extensions v3_ca -out ca.crt
# end ca

# pool cert
openssl genrsa -out pool.key 1024
openssl req -new -days 3650 -key pool.key -out pool.csr
openssl ca -in pool.csr -out pool.crt -cert ca.crt -keyfile ca.key -days 3650

echo "OK"
