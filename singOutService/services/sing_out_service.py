
from banking_fraud_lib.elasticsearchResource import ElasticSearchResource
from flask import Blueprint, jsonify
from resources.sing_out_service_response import SingOutServiceResponse
import boto3
import logging
import requests
import botocore.exceptions

class sing_out_service():

    def __init__(self, configuration):
        self.elasticsearch = ElasticSearchResource(configuration)
        self.client_id = configuration.aws['client_id']
        self.pool_id = configuration.aws['pool_id']
        self.AWS = boto3.client('cognito-idp', 
                                aws_access_key_id=configuration.aws['aws_access_key_id'],
                                  aws_secret_access_key=configuration.aws['aws_secret_access_key'],
                                    region_name=configuration.aws['region_name'])
        self.individual_index = "individual"
        
        
    
    def sing_out(self, token):
        try:
            cognito_response = self.AWS.global_sign_out(
                AccessToken= token
            )
            
            if cognito_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return SingOutServiceResponse().response({'result': f'El usuario cerró sesión exitosamente.'}, 200)
            else:
                return SingOutServiceResponse().response({'result': 'Error al cerrar sesión.'}, 422)
            
        except botocore.exceptions.ClientError as e: 
            if e.response['Error']['Code'] == 'NotAuthorizedException':
                return SingOutServiceResponse().response({'result': 'El usuario no se encuentra logeado.'},422)
            return SingOutServiceResponse().response({'result': 'Servicio no disponible, intentelo de nuevo más tarde.'}, 422)
        
       
       
    
   