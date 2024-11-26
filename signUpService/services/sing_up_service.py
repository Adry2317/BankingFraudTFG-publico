
from banking_fraud_lib.elasticsearchResource import ElasticSearchResource
from flask import Blueprint, jsonify
from resources.sing_up_service_response import SingUpServiceServiceResponse
from models.individual_model import IndividualModel
import boto3
import logging

class sing_up_service():

    def __init__(self, configuration):
        self.elasticsearch = ElasticSearchResource(configuration)
        self.client_id = configuration.aws['client_id']
        self.AWS = boto3.client('cognito-idp', 
                                aws_access_key_id=configuration.aws['aws_access_key_id'],
                                  aws_secret_access_key=configuration.aws['aws_secret_access_key'],
                                    region_name=configuration.aws['region_name'])
        self.individual_index = "individual"
        
        

    def sing_up(self, req_data):
        try:
            #Comprobamos si el usuario existe en la base de datos
            self.elasticsearch.connect()
            query = {"query": {"bool": {"must": [{"term": {"user.email.keyword": {"value": req_data['email']}}}]}}}
            logging.info(query)
            response = self.elasticsearch.search_document(query=query, index=self.individual_index)
            logging.info(response)

            #si el usuario no existe se crea el documento, con los datos dados
            if len(response['hits']['hits']) == 0:
                individual = IndividualModel().parse_response(req_data)
                #comprobar 200
                self.elasticsearch.index_data(body=individual.message, index=self.individual_index)
            elif  response['hits']['hits'][0]['_source']['register'] and not response['hits']['hits'][0]['_source']['email_confirmed']:
                return SingUpServiceServiceResponse().response({'result': f'El usuario {req_data["email"]} se encuentra registrado, pero no confirmado.'}, 422)
            else:
                return SingUpServiceServiceResponse().response({'result': 'El usuario ya se encuentra registrado, dirijase a iniciar sesión'}, 422)
            

            response = self.elasticsearch.search_document(query=query, index=self.individual_index)
            logging.info(response)
            #Realizamos el registro en cognito
            try:
                cognito_response = self.AWS.sign_up(
                    ClientId = self.client_id,
                    Username = req_data['email'],
                    Password=  req_data['password'],
                    UserAttributes=[
                        {
                            'Name': 'email',
                            'Value': req_data['email']
                        }
                    ]
                )
                
                if cognito_response['ResponseMetadata']['HTTPStatusCode'] != 200:
                    raise Exception

            except Exception as exc:
                logging.info(exc)
                response['hits']['hits'][0]['_source']['error'] = "Fallo al registrar el usuario."
                self.elasticsearch.update_document(index=self.individual_index, id=response['hits']['hits'][0]['_id'], body= response['hits']['hits'][0]['_source'])
                return SingUpServiceServiceResponse().response({'result': 'Servicio no disponible, intentelo de nuevo más tarde.'}, 422)

            #Actualizamos el documento del usuario.
            response['hits']['hits'][0]['_source']['register']=True
            response['hits']['hits'][0]['_source']['error'] = ""
            self.elasticsearch.update_document(index=self.individual_index, id=response['hits']['hits'][0]['_id'], body= response['hits']['hits'][0]['_source'])
            return SingUpServiceServiceResponse().response({'result': f'Registro del usuario {req_data["email"]} completado.'}, 200)

        except Exception as exc:
            logging.info(exc)
            return SingUpServiceServiceResponse().response({'result': 'Servicio no disponible, intentelo de nuevo más tarde.'}, 422)
        finally:
            self.elasticsearch.close_connection()
       
    
   