from app.api import requests
from app import app
from flask import render_template, request
import json


@app.route('/recomendar')
def recommend():
    """
    Esta view construye la página de en la que se muestra el formulario para
    solicitar recomendaciones. Solicita una muestra aleatoria de usuarios a
    la API para dar a elegir en el formulario.

    Returns:
        template: Código HTML generado.
    """
    return render_template('recommend.html',
                           name='Recommend',
                           random_users=requests.get_users())


@app.route('/get_recommendation', methods=['GET'])
def get_recommendation():
    """
    Esta view construye el código HTML que será incrustado en la parte inferior
    de la página de recomendación. Hace la llamada a la API solicitando el
    ranking de recomendación de cada algoritmo y construye las dos listas
    de noticias ordenadas.

    Args:
        user (:obj: `GET`): Id del usuario a recomendar.
        timestamp (:obj: `GET`): Timestamp de la fecha de acceso al sistema.
        algorithm1 (:obj: `GET`): Algoritmo A a utilizar.
        algorithm2 (:obj: `GET`): Algoritmo B a utilizar.

    Returns:
        template: Código HTML generado.
    """
    user = request.args.get('user')
    timestamp = request.args.get('timestamp')
    algorithm1 = request.args.get('algorithm1')
    algorithm2 = request.args.get('algorithm2')

    # Llamada a la API que solicita la recomendación
    news = json.loads(requests.get_recommendation(user,
                                                  timestamp,
                                                  algoritmo1=algorithm1,
                                                  algoritmo2=algorithm2))


    # Detecta si ha ocurrido un error en alguno de los algoritmos (una
    # recomendación repleta de ceros)
    if sum([i['alg1'] for i in news]) == 0 or sum([i['alg2'] for i in news]) == 0:
        print('Error en alguno de los algoritmos')
        return 'Error'

    # Se ordenan las noticias en base a las puntuaciones de cada algoritmo
    news_alg1 = enumerate(sorted(news, key=lambda x: x['alg1'], reverse=True))
    news_alg2 = enumerate(sorted(news, key=lambda x: x['alg2'], reverse=True))

    # Se genera el código HTML necesario
    return render_template('candidates.html',
                           algorithm1=algorithm1.upper(),
                           algorithm2=algorithm2.upper(),
                           news_alg1=news_alg1,
                           news_alg2=news_alg2)


@app.route('/carousel', methods=['GET'])
def carousel():
    """
    Esta view construye el código HTML que será incrustado en la parte central
    de la página de recomendación, en un carrusel interactivo. Hace la llamada
    a la API para obtener las noticias visitadas por ese usuario en un pasado
    y las muestra en grupos de dos en el carrusel.

    Args:
        user (:obj: `GET`): Id del usuario a recomendar.

    Returns:
        template: Código HTML generado.
    """
    user = request.args.get('user_id')

    if user is None:
        raise AttributeError("Error Parametros.")

    # Llamada  a la API
    news = json.loads(requests.get_clicked_news(user, details=True))

    # División en grupos
    group_size = 2
    news_groups = [news[i:i+group_size] for i in range(0, len(news), group_size)]

    # Se genera el código HTML necesario
    return render_template('carousel.html', name='Carousel', clicked_news=news_groups)
    