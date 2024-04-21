
import logging
from elasticsearch import Elasticsearch

class ElasticSearchResource():
    def __init__(self, configuration=None) -> None:
        self.elastic_settings = configuration.elasticSettings
        self.elastic_search_client = None

    def connect(self):
        try:
            logging.info("Comienza la conexión con elasticsearch")
            self.elastic_search_client = Elasticsearch(self.elastic_settings['node'], timeout=60,max_retries=3)
        except Exception:
            raise Exception(f"Error al conectar al nodo {self.elastic_settings['node']}")
        
    def close_connection(self):
        try:
            logging.info("Se cierra la conexión con el nodo")
            self.elastic_search_client.close()
        except Exception:
            raise Exception(f"Error al cerrar la conexión con el nodo {self.elastic_settings['node']}")
    

    def index_data(self, body, index, refresh='true'):
        try:
            logging.info(f"Empezando a indexar datos en {index}")

            self.elastic_search_client.index(index=index, body=body, refresh=refresh)
        
        except Exception as exc:
            raise Exception(f"Error al indexar datos dentro de {index}: {exc}")
        
    def update_document(self, index, id, body, refresh = "true"):
        try:
            logging.info("Empieza la actualización del documento")
            self.elastic_search_client.update(index=index, doc=body, id=id, refresh=refresh)
        except Exception as exc:
            raise Exception(f"Error al actualizar el documento en {index}: {exc}")
    
    def search_document(self, index, query):
        try:
            logging.info(f"Se inicia la busqueda del documento en {index}")
            return self.elastic_search_client.search(index=index, body=query)
        except Exception:
            raise Exception(f"Fallo al buscar el documento en {index}")
    
    def delete_document(self, index, id_doc):
        try:
            logging.info(f"Se inicia el borrado del documento en {index}")
            self.elastic_search_client.delete(index=index, id=id_doc)
        except Exception:
            raise Exception(f"Fallo al borrar el documento en {index}")