from banking_fraud_lib.elasticsearchResource import ElasticSearchResource
from flask import Blueprint, jsonify
from resources.sing_up_service_response import SingUpServiceServiceResponse
from botocore.exceptions import ClientError
import boto3
import logging

class singUpConfirmService():

    def __init__(self, configuration) -> None:
        self.elasticsearch = ElasticSearchResource(configuration)
        self.client_id = configuration.aws['client_id']
        self.pool_id = configuration.aws['pool_id']
        self.AWS = boto3.client('cognito-idp', 
                                aws_access_key_id=configuration.aws['aws_access_key_id'],
                                  aws_secret_access_key=configuration.aws['aws_secret_access_key'],
                                    region_name=configuration.aws['region_name'])
        self.individual_index = "individual"

    def confirm_email(self, req_data):
        try:
            #Comprobamos si el usuario existe en la base de datos
            self.elasticsearch.connect()
            query = {"query": {"bool": {"must": [{"match": {"user.email": req_data['email']}}]}}}
            response = self.elasticsearch.search_document(query=query, index=self.individual_index)

            if len(response['hits']['hits']) == 0:
                 return SingUpServiceServiceResponse().response({'result': 'El usuario no se encuentra dentro del sistema.'}, 422)
            
            response_doc = response['hits']['hits'][0]

            if not response_doc['_source']['register']:
                 return SingUpServiceServiceResponse().response({'result': 'El usuario no ha terminado el registro en el sistema.'}, 422)
            elif response_doc['_source']['email_confirmed']:
                 return SingUpServiceServiceResponse().response({'result': 'El usuario ya se encuentra registrado, dirijase a iniciar sesión'}, 422)

            try:
                cognito_response = self.AWS.confirm_sign_up(
                    ClientId = self.client_id,
                    Username = req_data['email'],
                    ConfirmationCode=req_data['code']
                )

                
                if cognito_response['ResponseMetadata']['HTTPStatusCode'] != 200:
                    raise Exception
            
            
            except ClientError as e:
                if e.response['Error']['Code'] == 'CodeMismatchException':
                    return SingUpServiceServiceResponse().response({"result": "Código de confirmación no válido. Por favor, inténtalo de nuevo."}, 422)
            except Exception as exc:
                logging.info(exc)
                response_doc['_source']['error'] = "Fallo al confirmar el usuario."
                self.elasticsearch.update_document(index=self.individual_index, id=response_doc['_id'], body= response_doc['_source'])
                return SingUpServiceServiceResponse().response({'result': 'Servicio no disponible, intentelo de nuevo más tarde.'}, 422)

            #Actualizamos la información del usuario.
            response_doc['_source']['email_confirmed'] = True
            response_doc['_source']['user_credentials']['username'] = req_data['email']
            self.elasticsearch.update_document(index=self.individual_index, id=response_doc['_id'], body= response_doc['_source'])

            return SingUpServiceServiceResponse().response({"result": "Ususario confirmado correctamente"}, 200)


        except Exception as exc:
            logging.info(exc)
            return SingUpServiceServiceResponse().response({'result': 'Servicio no disponible, intentelo de nuevo más tarde.'}, 422)
        finally:
            self.elasticsearch.close_connection() 



    def resend_verification_code(self, req_data):

        try:
            #Comprobamos si el usuario existe en la base de datos
            self.elasticsearch.connect()
            query = {"query": {"bool": {"must": [{"match": {"user.email": req_data['email']}}]}}}
            response = self.elasticsearch.search_document(query=query, index=self.individual_index)

            if len(response['hits']['hits']) == 0:
                 return SingUpServiceServiceResponse().response({'result': 'El usuario no se encuentra dentro del sistema.'}, 422)
            
            response_doc = response['hits']['hits'][0]

            if not response_doc['_source']['register']:
                 return SingUpServiceServiceResponse().response({'result': 'El usuario no ha terminado el registro en el sistema.'}, 422)
            elif response_doc['_source']['email_confirmed']:
                 return SingUpServiceServiceResponse().response({'result': 'El usuario ya se encuentra registrado, dirijase a iniciar sesión'}, 422)
            

            cognito_response = self.AWS.resend_confirmation_code(
                ClientId = self.client_id,
                Username = req_data['email']
                
            )

            logging.info(cognito_response)

            if cognito_response['ResponseMetadata']['HTTPStatusCode'] != 200:
                    raise Exception
            
            return SingUpServiceServiceResponse().response({"result": "Código de confirmación reenviado con éxito."}, 200)

        except Exception as exc:
            logging.info(exc)
            return SingUpServiceServiceResponse().response({'result': 'Servicio no disponible, intentelo de nuevo más tarde.'}, 422)
        finally:
            self.elasticsearch.close_connection() 