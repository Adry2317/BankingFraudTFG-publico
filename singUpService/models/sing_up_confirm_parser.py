from resources.sing_up_service_response import SingUpServiceServiceResponse
import re

class singUpConfirmParser():

    def __init__(self) -> None:
        self.email = None
        self.code = None

    def parse_request(self, request):

        try:
            self.email = request['email']
            email_patern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_patern, self.email) is None:
                return SingUpServiceServiceResponse().response({"result": "El campo email no es correcto"}, 422)
        except:
            return SingUpServiceServiceResponse().response({"result": "El campo email es requerido"}, 422)
        

        try: 
            self.code = request['code']

            if isinstance(self.code, int):
                return SingUpServiceServiceResponse().response({"result": f"El campo code debe de ser str: {type(self.code)}"}, 422)

            if len(self.code) != 6:
                return SingUpServiceServiceResponse().response({"result": "El código solo puede contener 6 dígitos."}, 422)
            
        except:
            return SingUpServiceServiceResponse().response({"result": "El campo code es requerido"}, 422)
        
        return SingUpServiceServiceResponse().response(self.__dict__, 200)
    

    def parse_resend_request(self, request):
        try:
            self.email = request['email']
            email_patern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_patern, self.email) is None:
                return SingUpServiceServiceResponse().response({"result": "El campo email no es correcto"}, 422)
        except:
            return SingUpServiceServiceResponse().response({"result": "El campo email es requerido"}, 422)
        
        return SingUpServiceServiceResponse().response({"email":request["email"]}, 200)