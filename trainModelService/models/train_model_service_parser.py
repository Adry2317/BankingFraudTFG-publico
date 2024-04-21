from resources.train_model_service_response import TrainModelServiceResponse
import re, base64

class TrainModelServiceParser():

    def __init__(self) -> None:
        self.email = None
        self.csv_file = None
        self.model_name = None
        self.algorithm = None
        self.input_type = None
        self.objetive = None
        self.drop_column = None
        self.filtered_columns = None
    
    def parse_request(self, request, files):
        try:
            self.email = request.get('email')
            email_patern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_patern, self.email) is None:
                return TrainModelServiceResponse().response({"result": "El campo email no es correcto"}, 422)
        except:
            return TrainModelServiceResponse().response({"result": "El campo email es requerido"}, 422)
        

        try:
            if 'csv_model' not in files:
                return TrainModelServiceResponse().response({'result': 'No se ha proporcionado ningun archivo CSV.'}, 422)
            
            self.csv_file = files['csv_model']

            #comprobamos que el nombre del archivo no esté vacio.
            if self.csv_file.filename == "":
                return TrainModelServiceResponse().response({'result': 'No se seleccionó ningun archivo CSV'}, 422)
            
            if self.csv_file.seek(0, 2) ==0:
                return TrainModelServiceResponse().response({'result': 'El archivo está vacío.'}, 422)
            self.csv_file.seek(0)
        except:
            return TrainModelServiceResponse().response({'result': 'El archivo CSV para entrenar el modelo no ha sido proporcionado.'}, 422)   

        try:
            self.model_name = request.get('model_name')
            if self.model_name == "":
                return TrainModelServiceResponse().response({'result': 'El nombre del modelo no puede estar vacio'}, 422)

            if not isinstance(self.model_name, str):
                return TrainModelServiceResponse().response({'result': f'El nombre debe de ser una cadena de texto: {type(self.model_name)}'}, 422)

        except:
            return TrainModelServiceResponse().response({"result": "El campo model_name es requerido"}, 422)
        
        try: 
            self.algorithm = request.get("algorithm")
            if not isinstance(self.algorithm, str):
                return TrainModelServiceResponse().response({"result": f"El campo algorithm debe ser una cadena de texto: {type(self.algorithm)}"})
            
            if self.algorithm not in  ['LogisticRegression', 'DecisionTreeClassifier', 'RandomForestClassifier', 'GradientBoostingClassifier'] :
                return TrainModelServiceResponse().response({'result': "El Nombre del algoritmo no es correcto."}, 422)
        except:
            return TrainModelServiceResponse().response({"result": "El campo algorithm es requerido"}, 422)

        try:
            self.input_type = request.get('input_type')
            
            if not isinstance(self.input_type, str):
                return TrainModelServiceResponse().response({'result': f'La entrada del entreno debe de ser una cadena de texto: {type(self.model_name)}'}, 422)

        except:
            return TrainModelServiceResponse().response({"result": "La entrada del entreno es requerido"}, 422)

        try:
            self.objetive = request.get('objetive')
            if self.objetive == "":
                return TrainModelServiceResponse().response({'result': 'El objetivo del entreno no puede estar vacio'}, 422)

            if not isinstance(self.objetive, str):
                return TrainModelServiceResponse().response({'result': f'El objetivo del entreno debe de ser una cadena de texto: {type(self.model_name)}'}, 422)

        except:
            return TrainModelServiceResponse().response({"result": "El objetivo del entreno es requerido"}, 422)
        
        try:
            self.drop_column = request.get('drop_column').split(";")
        except:
            return TrainModelServiceResponse().response({"result": "El campo de columnas a eliminar es necesario."}, 422)
        
        try:
            self.filtered_columns = request.get('filtered_coulumns')
        except:
            return TrainModelServiceResponse().response({"result": "El filtro de columnas es necesario."}, 422)

        return TrainModelServiceResponse().response(self.__dict__, 200)