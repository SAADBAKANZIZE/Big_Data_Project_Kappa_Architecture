from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType

# Initialiser la session Spark
spark = SparkSession.builder.appName("WriteToElasticsearch").getOrCreate()

# Créer un schéma pour le DataFrame
schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("comment", StringType(), True),
    StructField("sentiment", StringType(), True),
])

# Charger tous les fichiers JSON dans le répertoire spécifié
json_data_stream = spark.read \
    .schema(schema) \
    .json("/usef/data/data.json/part-00000-c86a53d7-f3ad-4dce-9ba4-e11b00a3a312-c000.json")

# Convertir la colonne "timestamp" en format timestamp
json_data_stream = json_data_stream.withColumn("timestamp", col("timestamp").cast(TimestampType()))

# Convertir la colonne "sentiment" en type entier
json_data_stream = json_data_stream.withColumn("sentiment", col("sentiment").cast(IntegerType()))

# Configurer les paramètres Elasticsearch
es_config = {
    "es.nodes": "demo2-elasticsearch-1",
    "es.port": "9200",
    "es.resource": "spark5",
    "es.write.operation": "index",
}

# Enregistrer le DataFrame dans Elasticsearch
json_data_stream.write \
    .format("org.elasticsearch.spark.sql") \
    .options(**es_config) \
    .mode("append") \
    .save()

# Arrêter la session Spark
spark.stop()
