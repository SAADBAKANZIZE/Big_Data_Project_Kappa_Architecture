## Real-Time Sentiment Analysis with Kappa Architecture
#Project Overview
This project focuses on implementing a Kappa architecture for real-time sentiment analysis using a combination of Apache Kafka, Apache NiFi, Elasticsearch, and Kibana. It falls under the domain of big data analytics and leverages various technologies to achieve real-time insights.

# Kappa Architecture
The Kappa architecture is a paradigm for processing and analyzing real-time data. It simplifies the traditional Lambda architecture by using a unified stream processing system for both batch and real-time data. In our implementation, we employ the Kappa architecture to enable efficient and scalable real-time sentiment analysis.
![image](https://github.com/SAADBAKANZIZE/Big_Data_Project_Kappa_Architecture/assets/101594125/0c141a05-f6d0-4639-a319-edef7349b12c)


## Technologies Used
![image](https://github.com/SAADBAKANZIZE/Big_Data_Project_Kappa_Architecture/assets/101594125/738278ee-275f-44cb-9040-9c9358acb988)

# 1. Apache Kafka
Apache Kafka serves as the central component for building real-time data pipelines. It facilitates the ingestion, storage, and streaming of data efficiently, ensuring robust and scalable processing.

# 2. Spark Streaming and Spark ML
Spark Streaming is employed for real-time data processing, while Spark ML (Machine Learning) is utilized for sentiment analysis. These technologies enable the extraction of valuable insights from the streaming data in real time.

# 3. Elasticsearch
Elasticsearch is a powerful search and analytics engine used to store and query large volumes of data quickly. It serves as the repository for processed data in our architecture.

# 4. Kibana
Kibana is utilized as the visualization layer, providing a user-friendly interface to explore and visualize the results of sentiment analysis stored in Elasticsearch.
# 5. Docker
Docker is employed to containerize our application components, ensuring consistency and reproducibility across different environments. The use of Docker simplifies the deployment process, making it easier to manage dependencies and scale our solution efficiently.
## Data Source
The project utilizes the YouTube API to retrieve data for sentiment analysis. Leveraging the YouTube API enables us to access real-time comments and reactions, contributing to the continuous flow of data for analysis.

## Contributors
Bakanzize Saad
Kadiri Youssef


