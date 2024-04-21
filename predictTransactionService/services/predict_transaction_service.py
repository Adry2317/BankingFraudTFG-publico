
from banking_fraud_lib.elasticsearchResource import ElasticSearchResource
from flask import Blueprint, jsonify
from resources.predict_transaction_service_response import PredictTransactionResponse
import logging
from datetime import datetime
import base64, pickle
import pandas as pd
import uuid


class PredictTransactionservice():

    def __init__(self, configuration):
        self.elasticsearch = ElasticSearchResource(configuration)
        self.trainig_model_index = "training_model"
        self.transaction_history_index = "transaction_history"

        
    
    def predict_transaction(self, req_data, username):
        try:
            self.elasticsearch.connect()
            query = {"query": {"bool": {"must": [{"match": {"user": username}}]}}}
            response = self.elasticsearch.search_document(query=query, index=self.trainig_model_index)
            flag_models = False
           

            if len(response['hits']['hits']) > 0:
                model_data = None
                models_doc = response['hits']['hits'][0]['_source']
                for model in models_doc['model']:
                    if req_data['model_name'] == model['model_name'] and req_data['algorithm'] == model['algorithm']:
                        model_data = model
                        flag_models = True
                        break
                
            if not flag_models:
                return PredictTransactionResponse().response({"result": f"No ha sido posible encontrar el modelo: {req_data['model_name']} con el tipo de algoritmo: {req_data['algorithm']}, para el usuario: {username}"}, 422)

            
            #Procedemos a cargar el modelo:
            model_bytes_decode = base64.b64decode(model_data['model_data'])
            model = pickle.loads(model_bytes_decode)
            df = pd.DataFrame([req_data['transaction']])
            df.drop(columns=req_data['drop_colum'],inplace=True)
            prediction = model.predict(df)

            #indexamos la transaccion
            doc = {
                "user": username,
                "model_name": req_data['model_name'],
                "algorithm": req_data['algorithm'],
                "transaction": req_data['transaction'],
                "prediction": "Fraudulent" if int(prediction) == 1 else "Legitimate",
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            }

            self.elasticsearch.index_data(body=doc, index=self.transaction_history_index)
            
            return PredictTransactionResponse().response({'result': doc}, 200)

        except Exception as exc:
            logging.info(exc)
            return PredictTransactionResponse().response({'result': 'Servicio no disponible, intentelo de nuevo más tarde.'}, 422)
        finally:
            self.elasticsearch.close_connection()
        
       
       
    
   