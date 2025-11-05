# Stack ELK avec Dashboard et Données Fictives

Ce projet contient une configuration complète de la stack ELK (Elasticsearch, Logstash, Kibana) avec un générateur de données fictives pour démonstration.

## 📋 Prérequis

- **Docker** et **Docker Compose** installés
- **Python 3.8+** (pour le générateur de données)
- Au moins **4 GB de RAM** disponibles pour Docker

## 🚀 Installation rapide

### 1. Cloner le projet

`bash
git clone <votre-repo>
cd elk-stack-demo
`

### 2. Structure du projet

Créez la structure suivante :

`elk-stack-demo/
├── docker-compose.yml
├── logstash/
│   ├── config/
│   │   └── logstash.yml
│   └── pipeline/
│       └── logstash.conf
├── generate_fake_data.py
├── requirements.txt
└── README.md`

### 3. Créer les fichiers de configuration

Créez le dossier pour Logstash :

`bash
mkdir -p logstash/config logstash/pipeline
`

Copiez les configurations fournies dans les artifacts correspondants.

### 4. Installer les dépendances Python

`bash
pip install -r requirements.txt
`

**Fichier
equirements.txt :**
`faker==20.1.0`

### 5. Démarrer la stack ELK

`bash
docker-compose up -d
`

**Vérifier que tout fonctionne :**

`bash
docker-compose ps
`
<img width="1725" height="909" alt="image" src="https://github.com/user-attachments/assets/ff4f5ac7-d20f-4df5-8781-2344fa09304d" />
<img width="455" height="493" alt="image" src="https://github.com/user-attachments/assets/9464bfc7-4c57-44ea-8e14-c1516f353bb6" />
<img width="426" height="419" alt="image" src="https://github.com/user-attachments/assets/2c3a8480-16c9-4ca9-b936-1296e8f34145" />

Vous devriez voir 3 conteneurs en cours d'exécution.

### 6. Attendre que tout soit prêt

Attendez environ 1-2 minutes que tous les services démarrent. Vérifiez :

- **Elasticsearch** : http://localhost:9200
- **Kibana** : http://localhost:5601

### 7. Générer des données fictives

`bash
python generate_fake_data.py
`
Le script va envoyer 100 logs fictifs à Logstash.
<img width="844" height="803" alt="image" src="https://github.com/user-attachments/assets/57dc3dfb-7ba3-498b-9e5b-cb03b5b75e38" />

## 📊 Créer un Dashboard dans Kibana

### Étape 1 : Accéder à Kibana

Ouvrez votre navigateur : http://localhost:5601

### Étape 2 : Créer un Data View

1. Menu hamburger (☰) → **Management** → **Stack Management**
2. Sous **Kibana**, cliquez sur **Data Views**
3. Cliquez sur **Create data view**
4. Configurez :
   - **Name** : logs-\*
   - **Index pattern** : logs-\*
   - **Timestamp field** : @timestamp
5. Cliquez sur **Save data view to Kibana**

### Étape 3 : Explorer les données

1. Menu hamburger → **Analytics** → **Discover**
2. Sélectionnez le data view logs-\*
3. Vous verrez tous vos logs !

### Étape 4 : Créer des visualisations

1. Menu hamburger → **Analytics** → **Visualize Library**
2. Cliquez sur **Create visualization**
3. Exemples de visualisations :

#### Graphique : Logs par niveau

- Type : **Pie chart**
- Data view : logs-\*
- Slice by : level.keyword

#### Graphique : Logs par service au fil du temps

- Type : **Line chart**
- Horizontal axis : @timestamp
- Vertical axis : Count
- Break down by : service.keyword

#### Métrique : Total des erreurs

- Type : **Metric**
- Filtre : level: "ERROR"
- Metric : Count

### Étape 5 : Créer un Dashboard

1. Menu hamburger → **Analytics** → **Dashboard**
2. Cliquez sur **Create dashboard**
3. Cliquez sur **Add from library**
4. Ajoutez vos visualisations créées précédemment
5. Arrangez-les comme vous le souhaitez
6. Cliquez sur **Save** et donnez un nom à votre dashboard

## 🔧 Commandes utiles

### Arrêter la stack

`bash
docker-compose down
`

### Arrêter et supprimer les données

`bash
docker-compose down -v
`

### Voir les logs des conteneurs

`bash
docker-compose logs -f
`

### Voir les logs d'Elasticsearch

`bash
docker-compose logs -f elasticsearch
`

### Régénérer des données

`bash
python generate_fake_data.py
`

Modifiez NUM_LOGS = 100 dans le script pour générer plus ou moins de logs.

## 📈 Personnalisation

### Modifier les types de logs générés

Éditez generate_fake_data.py et modifiez les listes :

- LOG_LEVELS
- SERVICES
- HTTP_METHODS
- HTTP_CODES

### Ajouter des filtres Logstash

Éditez logstash/pipeline/logstash.conf dans la section ilter {}.

### Changer la configuration d'Elasticsearch

Modifiez les variables d'environnement dans docker-compose.yml sous le service elasticsearch.

## 🐛 Résolution de problèmes

### Elasticsearch ne démarre pas

**Erreur** : max virtual memory areas vm.max_map_count [65530] is too low

**Solution Linux/Mac** :
`bash
sudo sysctl -w vm.max_map_count=262144
`

**Solution Windows (WSL2)** :
`powershell
wsl -d docker-desktop sysctl -w vm.max_map_count=262144
`

### Impossible d'envoyer des données à Logstash

Vérifiez que Logstash est bien démarré :
`bash
docker-compose logs logstash
`

Vérifiez que le port 5000 est ouvert :
`bash
netstat -an | grep 5000
`

### Kibana ne charge pas

Attendez 1-2 minutes après le démarrage. Vérifiez les logs :
`bash
docker-compose logs kibana
`

## 📝 Exporter/Importer un Dashboard

### Exporter

1. Dashboard → Settings → Export dashboard
2. Téléchargez le fichier JSON

### Importer

1. Dashboard → Create dashboard → Import
2. Uploadez le fichier JSON

## 🎯 Prochaines étapes

- Ajouter plus de types de données (métriques, APM, etc.)
- Configurer des alertes
- Ajouter des dashboards pré-configurés
- Intégrer Filebeat pour des logs de fichiers
- Ajouter Metricbeat pour des métriques système

## 📚 Ressources

- [Documentation Elastic](https://www.elastic.co/guide/index.html)
- [Kibana Query Language (KQL)](https://www.elastic.co/guide/en/kibana/current/kuery-query.html)
- [Logstash Patterns](https://www.elastic.co/guide/en/logstash/current/plugins-filters-grok.html)

## 📄 Licence

MIT
