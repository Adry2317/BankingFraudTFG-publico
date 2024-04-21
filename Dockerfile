# Usa la imagen oficial de Python como base
FROM python:3.12

ADD /banking_fraud_lib /banking_fraud_lib

RUN pip install -e /banking_fraud_lib