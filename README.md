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


