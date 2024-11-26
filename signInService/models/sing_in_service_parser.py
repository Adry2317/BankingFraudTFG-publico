
from resources.sing_in_service_response import SingInServiceResponse
import re, base64

class SingInServiceParser():
    
    def __init__(self):
        self.email = None
        self.password = None
       

    def parse_request(self, request):
        
        try:
            self.email = request['email']
            email_patern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_patern, self.email) is None:
                return SingInServiceResponse().response({"result": "El campo email no es correcto"}, 422)
        except:
            return SingInServiceResponse().response({"result": "El campo email es requerido"}, 422)

        try:
            self.password =base64.b64decode(request['password']).decode('utf-8') 

            if self.password == "":
                return SingInServiceResponse().response({"result": "El campo surname no puede estar vacío"}, 422)
        except:
            return SingInServiceResponse().response({"result": "El campo surname es requerido"}, 422)

        parsed_data = self.__dict__
        
        return SingInServiceResponse().response(parsed_data, 200)