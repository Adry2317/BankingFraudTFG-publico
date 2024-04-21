from flask import Flask
from resources.sing_up_service_error_handler import handle_key_error
from routes.sing_up_service_routes import sing_up_service_router
from banking_fraud_lib.configuration import Configuration
from flask_swagger_ui import get_swaggerui_blueprint


configuration = Configuration('config.ini')


app = Flask(__name__)
app.register_blueprint(sing_up_service_router)
#app.register_error_handler(KeyError, handle_key_error)

SWAGGER_URL = '/api/docs'  
API_URL = '/documentation'  



swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, 
    API_URL,
    config={  
        'app_name': "Banking Fraud"
    }
)

app.register_blueprint(swaggerui_blueprint)

@app.route('/documentation')
def swagger_json():
    try:
        with open('swagger.json', 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return {"error": "El archivo swagger.json no se encontró"}, 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5190)