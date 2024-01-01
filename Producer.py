import time
from confluent_kafka import Producer
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langdetect import detect

# Configurez la clé API YouTube et la requête de recherche
youtube_api_key = "AIzaSyCco5U0wY2ab4Q1BOANomyPOAcQY5WaFcI"
product_query = "Lucifer"

# Configurez le producteur Kafka
kafka_broker = 'localhost:29092'  # Remplacez par votre broker Kafka
kafka_topic = 'topic5'  # Remplacez par votre topic Kafka
producer = Producer({'bootstrap.servers': kafka_broker})

def is_english(comment):
    try:
        return detect(comment) == 'en'
    except:
        return False

def search_videos(api_key, query, max_results=10):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.search().list(
            q=query,
            part="id",
            maxResults=max_results,
            type="video"
        )
        response = request.execute()
        video_ids = [item['id']['videoId'] for item in response['items'] if 'id' in item and 'videoId' in item['id']]
        return video_ids
    except HttpError as e:
        error_details = e.error_details[0]
        print(f"Erreur dans search_videos : {error_details}")
        return []

def retrieve_video_comments(api_key, video_id, max_results=10):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=max_results
        )
        response = request.execute()
        comments_data = [
            {
                'timestamp': item['snippet']['topLevelComment']['snippet']['publishedAt'],
                'comment': item['snippet']['topLevelComment']['snippet']['textDisplay']
            } for item in response['items']
        ]
        english_comments = [comment for comment in comments_data if is_english(comment['comment'])]
        return english_comments
    except HttpError as e:
        error_details = e.error_details[0]
        if 'reason' in error_details and error_details['reason'] == 'commentsDisabled':
            print(f"Les commentaires sont désactivés pour la vidéo avec l'ID : {video_id}")
            return []
        else:
            raise

def delivery_report(err, msg):
    if err is not None:
        print('Échec de la livraison du message : {}'.format(err))
    else:
        print('Message livré à {} [{}]'.format(msg.topic(), msg.partition()))

def produce_youtube_comments():
    while True:
        # Recherchez les vidéos YouTube liées à la requête "jeep"
        video_ids = search_videos(youtube_api_key, product_query)

        # Récupérez les commentaires pour chaque vidéo
        for video_id in video_ids:
            video_comments = retrieve_video_comments(youtube_api_key, video_id)

            # Envoyez les commentaires à Kafka
            for comment in video_comments:
                producer.produce(kafka_topic, json.dumps(comment), callback=delivery_report)
                producer.flush()

        # Attendre avant de récupérer les données à nouveau (toutes les 30 secondes)
        time.sleep(30)

if __name__ == '__main__':
    produce_youtube_comments()
