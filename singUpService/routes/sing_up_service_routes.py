from flask import Blueprint, jsonify, request
from banking_fraud_lib.configuration import Configuration
from models.sing_up_service_parser import SingUpServiceParser
from models.sing_up_confirm_parser import singUpConfirmParser
from services.sing_up_service import sing_up_service
from services.sing_up_confirm_service import singUpConfirmService
import logging
import base64, json,re

configuration = Configuration("config.ini")

sing_up_service_router = Blueprint(
    'sing_up_service_router',  __name__, url_prefix='/bankingFraud'
)



@sing_up_service_router.post('/singUp')
def sing_up():
    logging.info('Starting connection with singUp service.')

    service = sing_up_service(configuration)

    req = request.get_json(force=True)
    
    parser = SingUpServiceParser().parse_request(req)
    
    if parser.status_code != 200:
        return jsonify(parser.message), parser.status_code
    
    
    response = service.sing_up(parser.message)
    
    
    return jsonify(response.message), response.status_code
   

@sing_up_service_router.post('/singUp/confirm')
def confirm_email():
    logging.info('Starting connection with singUp confirm service.')

    service = singUpConfirmService(configuration)

    req = request.get_json(force=True)

    parser = singUpConfirmParser().parse_request(req)

    if parser.status_code != 200:
        return jsonify(parser.message), parser.status_code
    
    response = service.confirm_email(parser.message)

    return jsonify(response.message), response.status_code


@sing_up_service_router.post('/singUp/resend_code')
def resend_verification_code():
    logging.info('Starting connection with resend_code service.')

    service = singUpConfirmService(configuration)
    
    req = request.get_json(force=True)

    parser = singUpConfirmParser().parse_resend_request(req)

    if parser.status_code != 200:
        return jsonify(parser.message), parser.status_code
    
    response = service.resend_verification_code(parser.message)

    return jsonify(response.message), response.status_code
