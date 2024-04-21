from functools import wraps
from flask import request, jsonify
from datetime import datetime
from jose import jwt, jwk
from jose.utils import base64url_decode
import time
import logging
import requests
import boto3, botocore

class CognitoResources():
    
    def __init__(self, configuration) -> None:
        self.user_pool_name = 'BankingFraud'
        self.token = None 
        self.AWS = boto3.client('cognito-idp', 
                                aws_access_key_id=configuration.aws['aws_access_key_id'],
                                  aws_secret_access_key=configuration.aws['aws_secret_access_key'],
                                    region_name=configuration.aws['region_name'])
    
    def login_required(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            
            token_data = request.headers.get('Authorization')
            if not token_data:
                return jsonify("Token de cognito no proporcionado"), 401
            
            self.token = token_data.split(" ")[1]
            
            try:
                token_header = jwt.get_unverified_header(self.token)
               

                # Decode token payload
                token_claims = jwt.get_unverified_claims( self.token)
                r = requests.get('https://cognito-idp.eu-north-1.amazonaws.com/eu-north-1_xQMwELRAJ/.well-known/jwks.json')
                if r.status_code == 200:
                    jwks = r.json()
                else:
                    raise 'Did not retrieve JWKS, got {}'.format(r.status_code)
            
                kid = token_header['kid']
                
                key_index = -1
                for i in range(len(jwks['keys'])):
                    if kid == jwks['keys'][i]['kid']:
                        key_index = i
                        break
                if key_index == -1:
                    return jsonify("No se ha encontrado una clave pública, por lo que no se ha podido verificar el token"), 401
                    
                else:
                    # Convert public key
                    public_key = jwk.construct(jwks['keys'][key_index])
                    # Get claims and signature from token
                    claims, encoded_signature =  self.token.rsplit('.', 1)
                    # Verify signature
                    decoded_signature = base64url_decode(
                            encoded_signature.encode('utf-8'))
                    if not public_key.verify(claims.encode("utf8"),
                                            decoded_signature):
                        return jsonify("Verificación de firma de cognito fallida"), 401
                        
                    else:

                        current_time = int(time.time())
                       
                        
                        if 'exp' in token_claims and current_time > token_claims['exp']:
                            return jsonify("Vuelva a iniciar sesión, tiempo expirado"), 401
                        
                        try:
                            self.token_user()
                        except Exception as e:
                            return jsonify(str(e)), 401
                        
                return func(*args, **kwargs)       
            except Exception as exc:
                logging.info(exc)
                raise Exception
        return decorated
        
        
    
    def token_user(self):
        try:
            cognito_response = self.AWS.get_user(
                AccessToken=self.token
            )
            for atributes in cognito_response['UserAttributes']:
                if atributes['Name'] == 'email':
                    return atributes['Value']
       
        except botocore.exceptions.ClientError as e:
             if e.response['Error']['Code'] == 'NotAuthorizedException':
               raise Exception('El usuario no se encuentra logueado.')
             else:
                 raise Exception('El usuario no se encuentra entre los usuarios activos.')
