from flask import Blueprint, jsonify, request
from banking_fraud_lib.configuration import Configuration
from banking_fraud_lib.cognitoResource import CognitoResources
from services.sing_out_service import sing_out_service
import logging
import csv
import base64, json,re

configuration = Configuration("config.ini")
cognito = CognitoResources(configuration)

sing_out_service_router = Blueprint(
    'sing_out_service_router',  __name__, url_prefix='/bankingFraud'
)


@sing_out_service_router.post('/singOut')
@cognito.login_required
def sing_up():
    logging.info('Starting connection with singOut service.')

    token = cognito.token
    response = sing_out_service(configuration).sing_out(token)
        
    logging.info('Finishing connection with singOut service.')
    return jsonify(response.message), response.status_code
   
