from resources.predict_transaction_service_response import PredictTransactionResponse
import re, base64

class PredictTransactionParser():

    def __init__(self) -> None:
        self.model_name = None
        self.algorthm = None
        self.drop_colum = None
        self.transaction = {
            'type': None,
            'amount': None,
            'nameOrig': None,
            'oldbalanceOrg': None,
            'newbalanceOrig': None,
            'nameDest': None,
            'oldbalanceDest': None,
            'newbalanceDest': None

        }
       
    
    def parse_request(self, req_data):

        try:
            self.model_name = req_data['model_name']

            if not isinstance(self.model_name, str):
                return PredictTransactionResponse().response({"result": f"El tipo del campo model_name debe de ser numerico: {type(self.model_name)}"}, 422)

        except:
            return PredictTransactionResponse().response({"result": "El campo model_name es requerido."}, 422)
        
        try:
            self.drop_colum = req_data['drop_colum'].split(";")

            if not isinstance(self.drop_colum, list):
                return PredictTransactionResponse().response({"result": f"El tipo del campo drop_colum debe de ser una lista: {type(self.drop_colum)}"}, 422)

        except:
            return PredictTransactionResponse().response({"result": "El campo drop_colum es requerido."}, 422)

        try: 
            self.algorithm = req_data["algorithm"]
            if not isinstance(self.algorithm, str):
                return PredictTransactionResponse().response({"result": f"El campo algorithm debe ser una cadena de texto: {type(self.algorithm)}"})
            
            if self.algorithm not in  ['LogisticRegression', 'DecisionTreeClassifier', 'RandomForestClassifier', 'GradientBoostingClassifier'] :
                return PredictTransactionResponse().response({'result': "El Nombre del algoritmo no es correcto."}, 422)
        except:
            return PredictTransactionResponse().response({"result": "El campo algorithm es requerido"}, 422)

        try:
            self.transaction['type'] = req_data['transaction']['type']
            
            if not isinstance(self.transaction['type'], str):
                return PredictTransactionResponse().response({"result": f"El tipo del dato debe de ser str: {type( self.transaction['type'])}"})
            
            if "TRANSFER" not in self.transaction['type']:
                return PredictTransactionResponse().response({"result": "La transacción debe de ser de tipo transferencia."},422)

        except:
            return PredictTransactionResponse().response({"result": "El campo type es requerido"},422)
        

        try:
            self.transaction['amount'] = req_data['transaction']['amount']

            if not isinstance(self.transaction['amount'], float):
                return PredictTransactionResponse().response({"result": f"El tipo del campo amount debe de ser numerico: {type(self.transaction['amount'])}"},422)

        except:
            return PredictTransactionResponse().response({"result": "El campo amount es requerido."},422)
        

        try:
            self.transaction['nameOrig'] = req_data['transaction']['nameOrig']

            if not isinstance(self.transaction['nameOrig'], str):
                return PredictTransactionResponse().response({"result": f"El tipo del campo nameOrig debe de ser str: {type(self.transaction['nameOrig'])}"}, 422)

        except:
            return PredictTransactionResponse().response({"result": "El campo nameOrig es requerido."}, 422)
        

        try:
            self.transaction['oldbalanceOrg'] = req_data['transaction']['oldbalanceOrg']

            if not isinstance(self.transaction['oldbalanceOrg'], float):
                return PredictTransactionResponse().response({"result": f"El tipo del campo oldbalanceOrg debe de ser numerico: {type(self.transaction['oldbalanceOrg'])}"}, 422)

        except:
            return PredictTransactionResponse().response({"result": "El campo oldbalanceOrg es requerido."}, 422)
        

        try:
            self.transaction['newbalanceOrig'] = req_data['transaction']['newbalanceOrig']

            if not isinstance(self.transaction['newbalanceOrig'] , float):
                return PredictTransactionResponse().response({"result": f"El tipo del campo newbalanceOrig debe de ser numerico: {type(self.transaction['newbalanceOrig'] )}"}, 422)

        except:
            return PredictTransactionResponse().response({"result": "El campo newbalanceOrig es requerido."}, 422)
        
        try:
            self.transaction['nameDest'] = req_data['transaction']['nameDest']

            if not isinstance(self.transaction['nameDest'] , str):
                return PredictTransactionResponse().response({"result": f"El tipo del campo nameDest debe de ser str: {type(self.transaction['nameDest'] )}"}, 422)

        except:
            return PredictTransactionResponse().response({"result": "El campo nameDest es requerido."}, 422)
        
        try:
            self.transaction['oldbalanceDest'] = req_data['transaction']['oldbalanceDest']

            if not isinstance(self.transaction['oldbalanceDest'] , float):
                return PredictTransactionResponse().response({"result": f"El tipo del campo oldbalanceDest debe de ser numérico: {type(self.transaction['oldbalanceDest'])}"}, 422)

        except:
            return PredictTransactionResponse().response({"result": "El campo oldbalanceDest es requerido."}, 422)
        

        try:
            self.transaction['newbalanceDest'] = req_data['transaction']['newbalanceDest']

            if not isinstance(self.transaction['newbalanceDest'] , float):
                return PredictTransactionResponse().response({"result": f"El tipo del campo newbalanceDest debe de ser numérico: {type(self.transaction['newbalanceDest'] )}"}, 422)

        except:
            return PredictTransactionResponse().response({"result": "El campo newbalanceDest es requerido."}, 422)


        return PredictTransactionResponse().response(self.__dict__, 200)