FROM python:3.12-slim
RUN head -c 200M /dev/urandom > /tmp/big.bin && rm /tmp/big.bin
