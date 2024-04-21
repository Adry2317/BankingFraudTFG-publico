
from banking_fraud_lib.elasticsearchResource import ElasticSearchResource
from flask import Blueprint, jsonify
from resources.train_model_service_response import TrainModelServiceResponse
import logging
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os, base64


class train_model_service():

    def __init__(self, configuration):
        self.elasticsearch = ElasticSearchResource(configuration)
        self.trainig_model_index = "training_model"

        
    
    def train_model(self, req_data):
        try:
            self.elasticsearch.connect()
            query = {"query": {"bool": {"must": [{"match": {"user": req_data['email']}}]}}}
            response = self.elasticsearch.search_document(query=query, index=self.trainig_model_index)
            flag_models = False
            logging.info(f"H{req_data['filtered_columns']}")

            #Comprobamos que ese usuario tenga modelos entrenados
            if len(response['hits']['hits']) > 0:
                flag_models = True
                models_doc = response['hits']['hits'][0]['_source']
                for model in models_doc['model']:
                    if req_data['model_name'] == model['model_name'] and req_data['algorithm'] == model['algorithm']:
                        return TrainModelServiceResponse().response({"result": f"El modelo {req_data['model_name']} ya ha sido entrenado para este usuario."}, 422)
                
            # Procesamos el archivo CSV y entrenamos el modelo.
            try:
                training_file = req_data['csv_file']
                df = pd.read_csv(training_file)
                
                #Eliminamos las columnas vacías.
                columns_with_nulls = df.columns[df.isnull().any()]
                
                if len(columns_with_nulls) > 0:
                    df_cleaned = df.dropna()
                    logging.info("Se han eliminado las columnas vacias del archivo.")
                    X = df_cleaned[df_cleaned[req_data['filtered_columns']] == req_data['input_type']]
                    
                else:
                        X = df[df[req_data['filtered_columns']] == req_data['input_type']]

                Y = X[req_data['objetive']]
                
                X.drop(req_data['drop_column'], axis = 1 , inplace=True)
                
                X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3)
                
                logging.info(X_test)
                #Seleccionamos algoritmo de clasificación
                match req_data['algorithm']:
                    case "LogisticRegression":
                        model = LogisticRegression()
                    case "DecisionTreeClassifier":
                        model = DecisionTreeClassifier()
                    case "RandomForestClassifier":
                        model = RandomForestClassifier()
                    case "GradientBoostingClassifier":
                        model = GradientBoostingClassifier()
                    
                model.fit(X_train, Y_train)

                predictions = model.predict(X_test)

                logging.info(f"El ratio de acierto es: {accuracy_score(Y_test, predictions)}")
            
                model_byte = pickle.dumps(model)
                model_string_codified = base64.b64encode(model_byte).decode('utf-8')
                if not flag_models:
                    body = {
                        "model": [{
                            "algorithm": req_data['algorithm'],
                            "model_name": req_data['model_name'],
                            "file_name": req_data['csv_file'].filename,
                            "model_data": model_string_codified
                        }],
                        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                        "user": req_data['email']
                    }

                    self.elasticsearch.index_data(body=body, index=self.trainig_model_index)    
                else:
                    response['hits']['hits'][0]['_source']['model'].append(
                        {
                            "algorithm": req_data['algorithm'],
                            "model_name": req_data['model_name'],
                            "file_name": req_data['csv_file'].filename,
                            "model_data": model_string_codified
                        }
                    )
                    self.elasticsearch.update_document(index=self.trainig_model_index, id=response['hits']['hits'][0]['_id'], body=response['hits']['hits'][0]['_source'])
                return TrainModelServiceResponse().response({"result": f"Ratio de acierto: {accuracy_score(Y_test, predictions)}"}, 200)
            except Exception as exc:
                logging.info(f"Error al procesar el archivo CSV: {str(exc)}")
                return TrainModelServiceResponse().response({"result": "Error al procesar el archivo CSV"}, 422)
                



        except Exception as exc:
            logging.info(exc)
            return TrainModelServiceResponse().response({'result': 'Servicio no disponible, intentelo de nuevo más tarde.'}, 422)
        finally:
            self.elasticsearch.close_connection()
        
       
       
    
   