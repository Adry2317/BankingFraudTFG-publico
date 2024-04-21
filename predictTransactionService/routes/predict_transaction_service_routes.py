from flask import Blueprint, jsonify, request
from banking_fraud_lib.configuration import Configuration
from banking_fraud_lib.cognitoResource import CognitoResources
from services.predict_transaction_service import PredictTransactionservice
from models.predict_transaction_service_parser import PredictTransactionParser
import logging


configuration = Configuration("config.ini")
cognito = CognitoResources(configuration)

predict_transaction_service_router = Blueprint(
    'predict_transaction_service_router',  __name__, url_prefix='/bankingFraud'
)


@predict_transaction_service_router.post('/predict_transaction')
@cognito.login_required
def train_model():
   
    logging.info('Starting connection with train model service.')

    req = request.get_json(force=True)
    
    parser = PredictTransactionParser().parse_request(req)

    try:
        username = cognito.token_user()
    except Exception as e:
        return jsonify(str(e)), 401

    if parser.status_code != 200:
        return jsonify(parser.message), parser.status_code
    
    service = PredictTransactionservice(configuration).predict_transaction(parser.message, username)
        
    logging.info('Finishing connection with train model service.')

    return jsonify(service.message), service.status_code  
    

    
   
