from app import app
from flask import render_template, request
import requests
from app.api import requests as api_requests
import json
import re

def remove_img_tags(text):
    """
    Esta función recibe una cadena de texto con código HTML y elimina todas las
    etiquetas de imágenes. Ya que casi todas las imágenes que contienen las
    noticias tienen los enlaces caidos.

    Args:
        text (:obj: `str`): Texto HTML de entrada.
    Returns:
        str: Texto sin etiquetas de imágenes.
    """
    clean_text = re.compile('<img.*?>')
    return re.sub(clean_text, '', text)

def remove_html_tags(text):
    """
    Esta función recibe una cadena de texto con código HTML y elimina todas las
    etiquetas HTML, dejando un texto completamente limpio.

    Args:
        text (:obj: `str`): Texto HTML de entrada.
    Returns:
        str: Texto sin etiquetas HTML.
    """
    clean_text = re.compile('<.*?>')
    return re.sub(clean_text, '', text)


@app.route('/')
def index():
    """
    Esta view construye la página principal de la página web, incluyendo una
    muestra aleatoria de noticias solicitadas a la API.

    Returns:
        template: Código HTML generado.
    """
    news = json.loads(api_requests.get_news_sample())

    return render_template('index.html', name='INDEX', news=news)

@app.route('/new', methods=['GET'])
def new():
    """
    Esta view construye la página mostrada al dar click para ver en detalle una
    noticia. Lee el cuerpo de la noticia directamente de la URL de Microsoft,
    limpia el texto y lo muestra junto con el titular de la noticia.

    Args:
        url (:obj: `GET`): URL al cuerpo de la noticia.
        title (:obj: `GET`): Titular de la noticia.

    Returns:
        template: Código HTML generado.
    """
    url = request.args.get('url')
    title = request.args.get('title')

    res = requests.get(url).content.decode('utf-8').replace("\r\n","")

    # Tratamos de quedarnos solo con el cuerpo del articulo, a veces la 
    # estructura es diferente y nos quedamos con todo, quitando los tags
    # innecesarios.
    try:
        start_article = res.index( "<article" ) 
        end_article = res.index("</article>") + len( "</article>" )

        article = res[start_article:end_article]
    except:
        article = remove_html_tags(res)


    return render_template('new.html',
                           body=remove_img_tags(article),
                           title=title)