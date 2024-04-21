import configparser
import logging
import sys, os 

class Configuration:
    def __init__(self, config) -> None:
        self.aws = None
        self.elasticSettings = None
        self.config = config
        self._readConfig()

    def _readConfig(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
     
        try:
            self.aws = {
                'aws_access_key_id' : config.get('Aws', 'aws_access_key_id'),
                'aws_secret_access_key' : config.get('Aws', 'aws_secret_access_key'),
                'region_name' : config.get('Aws', 'region_name'),
                'client_id' : config.get('Aws', 'client_id'),
                'pool_id': config.get('Aws', 'pool_id')
            }
        except Exception as exc:
            print(exc)
            raise Exception("Los parámetros de aws no estan definidos.")
        
        try:
            self.elasticSettings = {"node": config.get('Elasticsearch', 'url')}
        except Exception:
            raise Exception("Los parámetros de elastic no están definidos.")
        
        # Configurar el formato de los logs
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        
        # Crear un logger
        logger = logging.getLogger("generalLogger")

        # Configurar un manejador que envíe los logs a la salida estándar (stdout)
        handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(handler)  
        logger.info("Se inicializa el sistema del logs")