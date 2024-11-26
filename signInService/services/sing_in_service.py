
from banking_fraud_lib.elasticsearchResource import ElasticSearchResource
from flask import Blueprint, jsonify
from resources.sing_in_service_response import SingInServiceResponse

import boto3
import logging

class sing_in_service():

    def __init__(self, configuration):
        self.elasticsearch = ElasticSearchResource(configuration)
        self.client_id = configuration.aws['client_id']
        self.pool_id = configuration.aws['pool_id']
        self.AWS = boto3.client('cognito-idp', 
                                aws_access_key_id=configuration.aws['aws_access_key_id'],
                                  aws_secret_access_key=configuration.aws['aws_secret_access_key'],
                                    region_name=configuration.aws['region_name'])
        self.individual_index = "individual"
        
        

    def sing_in(self, req_data):
        try:
            #Comprobamos si el usuario existe en la base de datos
            self.elasticsearch.connect()
            query = {"query": {"bool": {"must": [{"match": {"user.email": req_data['email']}}]}}}
            response = self.elasticsearch.search_document(query=query, index=self.individual_index)
            
            # #si el usuario no existe se crea el documento, con los datos dados
            if len(response['hits']['hits']) == 0:
                return SingInServiceResponse().response({'result': f'El usuario {req_data["email"]} no se encuentra registrado.'}, 422)
            elif  response['hits']['hits'][0]['_source']['register'] and not response['hits']['hits'][0]['_source']['email_confirmed']:
                return SingInServiceResponse().response({'result': f'El usuario {req_data["email"]} se encuentra registrado, pero no confirmado.'}, 422)
            
            
            try:

                cognito_response = self.AWS.initiate_auth(
                    ClientId=self.client_id,
                    AuthFlow='USER_PASSWORD_AUTH',
                    AuthParameters={
                        'USERNAME': req_data['email'],
                        'PASSWORD': req_data['password']
                    }
                )
                if cognito_response['ResponseMetadata']['HTTPStatusCode'] != 200:
                    raise Exception
                
                access_token = cognito_response['AuthenticationResult']['AccessToken']

                res = {
                    'message': 'Inicio de sesión satisfactorio.',
                    'access_token': access_token
                }
                
                return SingInServiceResponse().response({'result': res}, 200)

            except Exception as exc:
                logging.info(exc)
                return SingInServiceResponse().response({'result': f'No se pudo iniciar sesión.'}, 422)
            

        except Exception as exc:
            logging.info(exc)
            return SingInServiceResponse().response({'result': 'Servicio no disponible, intentelo de nuevo más tarde.'}, 422)
        finally:
            self.elasticsearch.close_connection()
       
    
   