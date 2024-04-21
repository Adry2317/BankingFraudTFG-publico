
from resources.sing_up_service_response import SingUpServiceServiceResponse
import re, base64

class SingUpServiceParser():
    
    def __init__(self):
        self.name = None
        self.surname = None
        self.email = None
        self.password = None
       

    def parse_request(self, request):
        
        try:
            self.name = request['name']
            if request['name'] == "":
                return SingUpServiceServiceResponse().response({"result": "El campo name no puede estar vacío"}, 422)
        except:
            return SingUpServiceServiceResponse().response({"result": "El campo name es requerido"}, 422)

        try:
            self.email = request['email']
            email_patern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_patern, self.email) is None:
                return SingUpServiceServiceResponse().response({"result": "El campo email no es correcto"}, 422)
        except:
            return SingUpServiceServiceResponse().response({"result": "El campo email es requerido"}, 422)

        try:
            self.surname = request['surname']
            if self.surname == "":
                return SingUpServiceServiceResponse().response({"result": "El campo surname no puede estar vacío"}, 422)
        except:
            return SingUpServiceServiceResponse().response({"result": "El campo surname es requerido"}, 422)

        try:
            self.password =base64.b64decode(request['password']).decode('utf-8') 

            if self.password == "":
                return SingUpServiceServiceResponse().response({"result": "El campo surname no puede estar vacío"}, 422)
        except:
            return SingUpServiceServiceResponse().response({"result": "El campo surname es requerido"}, 422)

        parsed_data = self.__dict__
        
        return SingUpServiceServiceResponse().response(parsed_data, 200)