from flask import Blueprint, jsonify, request
from banking_fraud_lib.configuration import Configuration
from banking_fraud_lib.cognitoResource import CognitoResources
from services.manage_model_service import ManageModelservice
from models.manage_model_service_parser import ManageModelParser
import logging


configuration = Configuration("config.ini")
cognito = CognitoResources(configuration)

manage_model_service_router = Blueprint(
    'manage_model_service_router',  __name__, url_prefix='/bankingFraud'
)


@manage_model_service_router.get('/listModel')
@cognito.login_required
def list_model():
    
    logging.info('Starting connection with train model service.')
    try:
        username = cognito.token_user()
    except Exception as e:
        return jsonify(str(e)), 401
    
    service = ManageModelservice(configuration).list_model(username)
        
    logging.info('Finishing connection with train model service.')

    return jsonify(service.message), service.status_code  
    
@manage_model_service_router.post('/deleteModel')
@cognito.login_required
def delete_model():
    
    logging.info('Starting connection with train model service.')
    try:
        username = cognito.token_user()
    except Exception as e:
        return jsonify(str(e)), 401
    
    req = request.get_json(force=True)

    parser = ManageModelParser().parse_request(req)

    if parser.status_code != 200:
        return jsonify(parser.message), parser.status_code

    service = ManageModelservice(configuration).delete_model(username, parser.message)
        
    logging.info('Finishing connection with train model service.')

    return jsonify(service.message), service.status_code  

    
   
