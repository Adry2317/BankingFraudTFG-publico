from resources.manage_model_service_response import ManageModelResponse
import re, base64

class ManageModelParser():

    def __init__(self) -> None:
        self.model_name = None
        self.algorthm = None
        
    
    def parse_request(self, req_data):

        try:
            self.model_name = req_data['model_name']

            if not isinstance(self.model_name, str):
                return ManageModelResponse().response({"result": f"El tipo del campo model_name debe de ser numerico: {type(self.model_name)}"}, 422)

        except:
            return ManageModelResponse().response({"result": "El campo model_name es requerido."}, 422)
        
    

        try: 
            self.algorithm = req_data["algorithm"]
            if not isinstance(self.algorithm, str):
                return ManageModelResponse().response({"result": f"El campo algorithm debe ser una cadena de texto: {type(self.algorithm)}"})
            
            if self.algorithm not in  ['LogisticRegression', 'DecisionTreeClassifier', 'RandomForestClassifier', 'GradientBoostingClassifier'] :
                return ManageModelResponse().response({'result': "El Nombre del algoritmo no es correcto."}, 422)
        except:
            return ManageModelResponse().response({"result": "El campo algorithm es requerido"}, 422)

        
        return ManageModelResponse().response(self.__dict__, 200)