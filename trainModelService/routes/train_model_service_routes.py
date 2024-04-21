from flask import Blueprint, jsonify, request
from banking_fraud_lib.configuration import Configuration
from banking_fraud_lib.cognitoResource import CognitoResources
from services.train_model_service import train_model_service
from models.train_model_service_parser import TrainModelServiceParser
import logging
import csv
import base64, json,re

configuration = Configuration("config.ini")
cognito = CognitoResources(configuration)

train_model_service_router = Blueprint(
    'train_model_service_router',  __name__, url_prefix='/bankingFraud'
)


@train_model_service_router.post('/trainModel')
@cognito.login_required
def train_model():
    logging.info('Starting connection with train model service.')

    req_param = request.form
    files = request.files

    parser = TrainModelServiceParser().parse_request(req_param, files)

    if parser.status_code != 200:
        return jsonify(parser.message), parser.status_code
    
    service = train_model_service(configuration).train_model(parser.message)
        
    logging.info('Finishing connection with train model service.')
    return jsonify(service.message), service.status_code
   
