class SingInServiceResponse():

    def __init__(self):
        self.message = None
        self.status_code = 0

    def response(self, msg: str, status_code: int):
        self.message = msg
        self.status_code = status_code

        return self