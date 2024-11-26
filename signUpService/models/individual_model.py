from datetime import datetime
from resources.sing_up_service_response import SingUpServiceServiceResponse

class IndividualModel():

    def __init__(self) -> None:
        self.user = {
            "email": "",
            "name": "",
            "last_name": ""
        }
        self.user_credentials = {
            "username": ""
        }
        self.email_confirmed = False
        self.register = False
        self.error=""
        self.timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
    def parse_response(self, req_data):
        try:
            self.user = {
                "email": req_data['email'],
                "name": req_data['name'],
                'last_name': req_data['surname']

            }
            return SingUpServiceServiceResponse().response(self.__dict__, 200)
            
        except Exception:
            return SingUpServiceServiceResponse().response({'result': 'Faltan campos al generar el docuento individual'}, 422)