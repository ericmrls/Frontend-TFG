"""
En este módulo se implementan las peticiones necesarias para consumir de cada
una de las API que componen este proyecto.

API Requests
------------
"""

import requests
import os

from configparser import ConfigParser


config = ConfigParser()
config.read("app.conf")

HOST = "http://{}:{}".format(config["API_CONFIG"]['host'],
                      config["API_CONFIG"]['port'])

def send_get(host, service, params=None, headers={}):
    """
    Esta función envía una petición GET al servicio del host que se envía como
    argumento. Además se pueden enviar parámetros utilizando el diccionario que
    se envía como argumento.

    Args:
        host (:obj: `str`): Host al que se envía la petición.
        service (:obj: `str`): Servicio que se quiere solicitar.
        params (:obj: `dict`): Parámetros a enviar en la petición.
    Returns:
        response: La respuesta o None en caso de error.
    """
    if params is not None:
        param_str = '&'.join([f"{k}={v}" for k, v in params.items()])
        response = requests.get(f"{host}/{service}/?{param_str}",
                                 headers=headers)
    else:
        response = requests.get(f"{host}/{service}/",
                                 headers=headers)
    if response.ok:
        return response
    else:
        return None


def get_users(n:int=10, train:bool=False):
    """
    Esta función envía una petición GET a la API para solicitar una muestra de
    identificadores de usuarios del dataset.

    Args:
        n (:obj: `int`, optional): Tamaño de la muestra.
        train (:obj: `bool`, optional):
            Señaliza si queremos que la muestra sea de la partición de train o
            de la partición de test.
    Returns:
        response: Lista con los identificadores o None en caso de error.
    """
    return send_get(HOST, 'users', locals()).json()

def get_news_sample(n:int=10, train:bool=False):
    """
    Esta función envía una petición GET a la API para solicitar una muestra 
    aleatoria de noticias del dataset.

    Args:
        n (:obj: `int`, optional): Tamaño de la muestra.
        train (:obj: `bool`, optional):
            Señaliza si queremos que la muestra sea de la partición de train o
            de la partición de test.
    Returns:
        response: Lista con los identificadores o None en caso de error.
    """
    return send_get(HOST, 'news_sample', locals()).json()

def get_timestamps(user_id:str, train:bool=False):
    """
    Esta función envía una petición GET a la API para solicitar los diferentes
    timestamps en los que el usuario accedió al sistema.

    Args:
        user_id (:obj: `str`): Identificador del usuario.
        train (:obj: `bool`, optional):
            Señaliza si queremos que la muestra sea de la partición de train o
            de la partición de test.
    Returns:
        response: Lista con los timestamps o None en caso de error.
    """
    return send_get(HOST, 'timestamp', locals()).json()

def get_available_news(user_id:str, date:str, train:bool=False):
    """
    Esta función envía una petición GET a la API para solicitar las noticias
    mostradas (candidatas) a un usuario en un timestamp (date) concreto.

    Args:
        user_id (:obj: `str`): Identificador del usuario.
        date (:obj: `str`): Timestamp del momento en el que accede.
        train (:obj: `bool`, optional):
            Señaliza si queremos que la muestra sea de la partición de train o
            de la partición de test.
    Returns:
        response: Lista con las noticias o None en caso de error.
    """
    return send_get(HOST, 'available_news', locals()).json()

def get_clicked_news(user_id:str,
                     abs_limit:int=120,
                     train:bool=False,
                     details:bool=False):
    """
    Esta función envía una petición GET a la API para solicitar las noticias
    que ha clickado en un pasado un usuario.

    Args:
        user_id (:obj: `str`): Identificador del usuario.
        date (:obj: `str`): Timestamp del momento en el que accede.
        train (:obj: `bool`, optional):
            Señaliza si queremos que la muestra sea de la partición de train o
            de la partición de test.
    Returns:
        response: Lista con las noticias o None en caso de error.
    """
    return send_get(HOST, 'clicked_news', locals()).json()

def get_recommendation(user_id:str,
                       date:str,
                       algoritmo1:str='nrms',
                       algoritmo2:str='naml',
                       train:bool=False):
    """
    Esta función envía una petición GET a la API para solicitar una
    recomendación en base a los argumentos enviados.

    Args:
        user (:obj: `GET`): Id del usuario a recomendar.
        timestamp (:obj: `GET`): Timestamp de la fecha de acceso al sistema.
        algorithm1 (:obj: `GET`): Algoritmo A a utilizar.
        algorithm2 (:obj: `GET`): Algoritmo B a utilizar.
        train (:obj: `bool`, optional):
            Señaliza si queremos que la muestra sea de la partición de train o
            de la partición de test.

    Returns:
        response: Lista de recomendaciones.
    """

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("API_KEY", "TEST_API_KEY")}'
    }
    return send_get(HOST, 'recommendation', locals(), headers=headers).json()
