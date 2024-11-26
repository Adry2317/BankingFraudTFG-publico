from flask import Blueprint, jsonify, request
from banking_fraud_lib.configuration import Configuration
from models.sing_in_service_parser import SingInServiceParser
from services.sing_in_service import sing_in_service
import logging
import base64, json,re

configuration = Configuration("config.ini")

sing_in_service_router = Blueprint(
    'sing_in_service_router',  __name__, url_prefix='/bankingFraud'
)



@sing_in_service_router.post('/singIn')
def sing_up():
    logging.info('Starting connection with singIn service.')

    service = sing_in_service(configuration)

    req = request.get_json(force=True)
    
    parser = SingInServiceParser().parse_request(req)
    
    if parser.status_code != 200:
        return jsonify(parser.message), parser.status_code
    
    
    response = service.sing_in(parser.message)
    
    
    return jsonify(response.message), response.status_code
   
