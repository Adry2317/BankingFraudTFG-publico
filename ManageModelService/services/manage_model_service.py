
from banking_fraud_lib.elasticsearchResource import ElasticSearchResource
from flask import Blueprint, jsonify
from resources.manage_model_service_response import ManageModelResponse
import logging
from datetime import datetime
import base64, pickle
import pandas as pd
import uuid


class ManageModelservice():

    def __init__(self, configuration):
        self.elasticsearch = ElasticSearchResource(configuration)
        self.trainig_model_index = "training_model"
       

        
    
    def list_model(self, username):
        try:
            self.elasticsearch.connect()
            query = {"query": {"bool": {"must": [{"term": {"user.keyword": {"value": username}}}]}}}
            response = self.elasticsearch.search_document(query=query, index=self.trainig_model_index)
            
            if len(response['hits']['hits']) == 0:
                return ManageModelResponse().response({'result': f"No se ha encontrado ningun modelo para el usuario: {username}"},422)
            
            for model in response['hits']['hits'][0]['_source']['model']:
                model.pop('model_data')
            return ManageModelResponse().response({'result': response['hits']['hits'][0]['_source']}, 200)

        except Exception as exc:
            logging.info(exc)
            return ManageModelResponse().response({'result': 'Servicio no disponible, intentelo de nuevo más tarde.'}, 422)
        finally:
            self.elasticsearch.close_connection()
        
       
    def delete_model(self, username, req_data):
        try:
            self.elasticsearch.connect()
            query = {"query": {"bool": {"must": [{"match": {"user": username}}]}}}
            response = self.elasticsearch.search_document(query=query, index=self.trainig_model_index)
            
            flag_models = False
            if len(response['hits']['hits']) == 0:
                return ManageModelResponse().response({'result': f"No se ha encontrado ningun modelo para el usuario: {username}"},422)
            
            model_remove = None
            for model in response['hits']['hits'][0]['_source']['model']:
                if req_data['model_name'] == model['model_name'] and req_data['algorithm'] == model['algorithm']:
                    model_remove = model
                    flag_models = True
                    break

        
            if not flag_models:
                return ManageModelResponse().response({"result": f"No ha sido posible encontrar el modelo: {req_data['model_name']} con el tipo de algoritmo: {req_data['algorithm']}, para el usuario: {username}"}, 422)
            
            response['hits']['hits'][0]['_source']['model'].remove(model_remove)
            if len(response['hits']['hits'][0]['_source']['model']) > 0:
                self.elasticsearch.update_document(index=self.trainig_model_index, body=response['hits']['hits'][0]['_source'],id=response['hits']['hits'][0]['_id'])
            else:
                self.elasticsearch.delete_document(index=self.trainig_model_index, id_doc=response['hits']['hits'][0]['_id'])
            
            return ManageModelResponse().response({'result': f"Se ha eliminado el modelo: {req_data['model_name']}, entrenado con el algoritmo: {req_data['algorithm']}, para el usuario: {username}"}, 200)

        except Exception as exc:
            logging.info(exc)
            return ManageModelResponse().response({'result': 'Servicio no disponible, intentelo de nuevo más tarde.'}, 422)
        finally:
            self.elasticsearch.close_connection()
    
   