# TwitterApi-V2
Scraping de tweets usando el token "bearer-token" asociado a un proyecto en específico en el portal para developers de twitter https://developer.twitter.com/en/portal/projects/

# Motivación
Los proyectos open-source de scraping de tweets, tales como https://github.com/taspinar/twitterscraper, https://github.com/twintproject/twint  son excelentes debido a su capacidad ilimitada de recolectar información de twitter sin usar ninguna Api. Sin embargo no son sostenibles a través del tiempo y para efectos de realizar un proyecto de trabajo es mejor utilizar la Api que ofrece twitter, debido a que es más estable y seguro. También he observado que "tweepy" version 3, la api de twitter para Python, no brinda campos necesarios como el número de replies que tiene un tweet (reply_count) o el id del tweet que es tema de conversarción (conversation_tweet_id). Por eso se desarrolló este repositorio que nos permitirá extraer la mayor cantidad de campos necesarios por cada tweet bajo un término clave, usando solamente "bearer_token".


# Configuracion del Entorno
Para este caso se ha configurado un entorno de conda con la version 3.9.0 Python e instalando las siguientes bibliotecas.  
* requests==2.26.0
* pandas==1.3.4
```
conda create -n venv_twitter python==3.9.0
conda activate venv_twitter
pip install -r requirements.txt
```

# Uso del Script
Primeramente se debe modificar la clave "bearer_token" dentro del archivo `utils/config.py` o configurar una variable de entorno ya sea en windows o linux(ejm por comando , `export bearer_token='your token'`). También se debe configurar la zona horaria, ya que las fechas de los tweets cuando se hace la consulta mediante la api están en formato UTC por lo que se debe modificar la variable "timezone" dentro del archivo `utils/config.py`. Por ejemplo `timezone = pytz.timezone("America/Lima")` para Perú o `timezone = pytz.timezone("America/Santiago")` para Chile.

* --query   (-q): Argumento obligatorio para realizar la busqueda de tweets. Tambien captura los tweet referenciados, cuando el tweet es un retweet con comentario, retweet sin comentario y/o respuesta a algun tweet
* --since   (-s): Argumento opcional para indicar el inicio de la fecha de extracción "%Y-%m-%d %H:%M:%S".  Valor por default, la hora "00:00:00" del dia de extracción. 
* --until   (-u): Argumento opcional para indicar la fecha final de extracíon "%Y-%m-%d %H:%M:%S". Valor por default, la hora actual del sistema operativo.
* --since_id    : Argumento opcional para activar la opcion de extraer los tweets a partir del último id recolectado asociado a un "query" en especifico. Si se utiliza por primera vez, tomará en cuenta los tweets del día actual a partir de la hora "00:00:00".
* --output (-o): Argumento opcional para indicar la forma de cómo guardar los datos extraídos, ya sea como "csv", "pkl" o "json". Valor por default "csv".

``` 
python twitter_api_search.py --query "@bcrpoficial"
python twitter_api_search.py --query "bcrpoficial"  -s "2021-12-03 12:00:00" --output csv 
python twitter_api_search.py --query "bcrpoficial" --since "2021-12-03 12:00:00" -u "2021-12-03 15:00:00" -o json
python twitter_api_search.py -q "bcrpoficial" --since_id --output pkl
```
El resultado  de la recolección de tweets se encontrará en la carpeta `results`  de la forma  `f'tweets_{query}.{output}'`

# Campos Recolectados
### Tweets Fields
* necessary: tweet_id, tweet_url, created_at, text, source, conversation_tweet_id, lang
* public_metrics: retweet_count, reply_count, like_count, quote_count
* entities: urls_text, mentions, annotations, hashtags
* type: retweeted_id, replied_tweet_id,quoted_tweet_id
### Users Fields
* necessary: user_id, user_name, screen_name, date_joined, description, location
* other: verified, protected, profile_image_url, pinned_tweet_id
* replied: replied_user_id, replied_screen_name
* public_metrics: followers_count, following_count, tweet_count, listed_count
* entities: url_blog, urls_description, mentions_description, hashtags_description

# Limitaciones
Aunque se pueden ver con mayor detalle en la documentacion https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent#cURL . Los más principales son: 
* Solo se permite extrear tweets de los últimos 7 días.
* Como máximo se pueden recolectar 30 mil tweets en un intérvalo de 15 minutos.
* Otra limitante es que permite extraer a lo máximo 2 millones de tweets cada mes, ir al siguiente link para ver el porcentaje de tweets recolectados del total permitido https://developer.twitter.com/en/portal/dashboard.    
