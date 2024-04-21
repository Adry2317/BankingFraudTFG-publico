import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parents
VERSION = '0.0.1'
AUTHOR = 'Adrian Arboledas Fernandez'
AUTHOR_EMAIL = 'aaf00022@red.ujaen.es'
PACKAGE_NAME = 'banking_fraud_lib'
URL = 'https://github.com/Adry2317' 

LICENSE = 'MIT' #Tipo de licencia

#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
      'boto3',
      'elasticsearch',
      'urllib3',
      'flask',
      'gunicorn',
      'python-jose',
      'botocore',
      'requests',
      'pandas',
      'scikit-learn==1.3.2',
      'joblib',
      "flask-swagger-ui==4.11.1 ",
      "flasgger"
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)