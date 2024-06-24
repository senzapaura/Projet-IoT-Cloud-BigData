# Projet de Prédiction des Prix de l'Immobilier

Ce projet vise à prédire les prix de l'immobilier en utilisant une combinaison de Kafka pour le streaming de données, Spark pour le prétraitement des données, Cassandra pour le stockage, et Flask pour l'API. Le projet inclut plusieurs scripts pour gérer le traitement des données, le stockage, l'entraînement du modèle et le déploiement.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

- Python 3.6 ou supérieur
- Java 8 ou supérieur (nécessaire pour Apache Spark)
- Apache Kafka
- Apache Cassandra
- MongoDB
- Hadoop HDFS
- pip (installateur de paquets Python)

## Installation

### Étape 1 : Cloner le Répertoire

```bash
git clone https://github.com/senzapaura/house-price-prediction.git
cd house-price-prediction
```

### Étape 2 : Installer les Paquets Python Requis

Créez un environnement virtuel et installez les paquets requis en utilisant le fichier requirements.txt fourni.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


### Étape 3 : Démarrer Hadoop HDFS

Assurez-vous que Hadoop est installé et configuré. Démarrez les services HDFS.

```bash
start-dfs.sh
```
### Étape 4 : Démarrer Kafka

Assurez-vous que Kafka est installé et configuré. Démarrez le serveur Kafka.

```bash
kafka-server-start.sh /path/to/kafka/config/server.properties
```

### Étape 5 : Démarrer Cassandra

Assurez-vous que Cassandra est installé et configuré. Démarrez le serveur Cassandra.

```bash
cassandra -f
```

### Étape 5 : Démarrer Cassandra

Assurez-vous que Cassandra est installé et configuré. Démarrez le serveur Cassandra.

```bash
mongod --config /path/to/mongodb/config/mongod.conf
```

## Installation

### Étape 1 : Prétraiter les Données

Exécutez le script de prétraitement des données pour lire les données depuis Kafka, les traiter avec Spark, et les stocker dans Cassandra.

```bash
python house_data_preprocess.py
```

### Étape 2 : Lire les Données depuis HDFS et les Envoyer à Kafka

Exécutez le script pour lire les données immobilières depuis HDFS et les envoyer à Kafka.


```bash
python hdfs_house_read.py
```

### Étape 3 : Démarrer l'API Flask

Exécutez l'API Flask pour entraîner le modèle et faire des prédictions.

```bash
python house_price_api.py
```


### Étape 4 : Demander l'Entraînement du Modèle et les Prédictions

Exécutez le script pour récupérer les données de Cassandra, les envoyer à l'API Flask pour l'entraînement du modèle, et stocker les prédictions dans MongoDB.

```bash
python request_house_model.py
```

### Étape 5 : Recevoir les Données via MQTT et les Enregistrer dans HDFS

Exécutez le script de réception MQTT pour écouter les données immobilières entrantes et les enregistrer dans HDFS.

```bash
python house_data_receiver.py
```

### Étape 6 : Envoyer les Données via MQTT

Exécutez le script d'envoi MQTT pour envoyer les données immobilières depuis les fichiers locaux vers le broker MQTT.


```bash
python house_data_sender.py
```

## Description des Fichiers

house_data_preprocess.py : Prétraiter les données avec Spark et les stocker dans Cassandra.
hdfs_house_read.py : Lire les données depuis HDFS et les envoyer à Kafka.
house_price_api.py : API Flask pour entraîner et prédire les prix immobiliers.
request_house_model.py : Récupérer les données de Cassandra, entraîner le modèle avec l'API Flask, et stocker les prédictions dans MongoDB.
house_data_receiver.py : Recevoir les données via MQTT et les enregistrer dans HDFS.
house_data_sender.py : Envoyer les données via MQTT depuis les fichiers locaux vers le broker MQTT.
requirements.txt : Dépendances Python nécessaires pour le projet.


## Requirements

Le fichier requirements.txt contient toutes les dépendances Python nécessaires pour ce projet. Assurez-vous d'avoir un environnement virtuel activé avant d'installer ces dépendances.

Flask==2.0.1
Flask-Cors==3.0.10
pandas==1.3.3
scikit-learn==0.24.2
numpy==1.21.2
paho-mqtt==1.5.1
confluent-kafka==1.8.2
pyspark==3.1.2
cassandra-driver==3.25.0
hdfs==2.6.0
pymongo==3.12.1


## Notes Supplémentaires

- Assurez-vous que tous les services (Kafka, Cassandra, MongoDB, HDFS) sont en cours d'exécution avant d'exécuter les scripts.
- Ajustez les chemins de fichiers et les configurations dans les scripts selon votre configuration.
- Le data_lake_path dans HDFS doit être pré-créé, sinon le script tentera de le créer.


## Contacts


