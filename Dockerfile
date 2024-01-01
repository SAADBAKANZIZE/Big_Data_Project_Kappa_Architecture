FROM docker.io/bitnami/spark:3

# Installer les modules en tant qu'utilisateur root
USER root
RUN apt-get update && apt-get install -y wget

# Installer les modules Python
RUN pip install TextBlob
RUN pip install onnxruntime
RUN pip install pandas
RUN pip install onnxmltools
RUN pip install onnxconverter-common
RUN pip install tensorflow==2.13.1
RUN pip install pyarrow==1.0.0

RUN mkdir -p /opt/spark/jars/
RUN wget -O /opt/spark/jars/elasticsearch-hadoop-7.17.1.jar https://repo1.maven.org/maven2/org/elasticsearch/elasticsearch-hadoop/7.17.1/elasticsearch-hadoop-7.17.1.jar

# Changer l'utilisateur pour l'exécution de l'application
USER 1001