from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from textblob import TextBlob

# Initialisation de la session Spark
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()

# Configuration des serveurs Kafka
kafka_bootstrap_servers = "kafka-1:9092"  # Mettez à jour avec les adresses correctes
kafka_topic = "topic5"  # Mettez à jour avec le nom correct du topic Kafka

# Définition du schéma des données
commentSchema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("comment", StringType(), True),
])

# Lecture en continu des données depuis Kafka
commentsDF = (spark.readStream
              .format("kafka")
              .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
              .option("subscribe", kafka_topic)
              .option("startingOffsets", "earliest")
              .load()
              .selectExpr("CAST(value AS STRING)")
              .select(from_json("value", commentSchema).alias("data"))
              .select("data.*")
             )

# Conversion de la colonne "timestamp" en type TimestampType
commentsDF = commentsDF.withColumn("timestamp", col("timestamp").cast(TimestampType()))

# Définition d'une fonction UDF pour l'analyse du sentiment

def analyze_sentiment(comment):
    analysis = TextBlob(comment)
    return 1 if analysis.sentiment.polarity >= 0 else 0


# Enregistrement de la fonction UDF
analyze_sentiment_udf = udf(analyze_sentiment, StringType())

# Ajout d'une colonne "sentiment" à votre DataFrame
commentsDF = commentsDF.withColumn("sentiment", analyze_sentiment_udf(col("comment")))

# Enregistrement des données analysées dans un fichier JSON
query = (commentsDF
         .writeStream
         .outputMode("append")
         .format("json")  
         .option("checkpointLocation", "/usef/checkpoints") # Utilisation du format JSON # Spécifiez un chemin pour le checkpoint
         .option("path", "/usef/data/data.json")  # Spécifiez le chemin où enregistrer le fichier JSON
         .start()
         )

# Attente de la fin du flux en continu
query.awaitTermination()
