import json
import random
import socket
import time
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('fr_FR')

# Configuration
LOGSTASH_HOST = 'localhost'
LOGSTASH_PORT = 5000
NUM_LOGS = 100

# Types de logs possibles
LOG_LEVELS = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
SERVICES = ['api', 'web', 'database', 'cache', 'queue', 'auth']
HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
HTTP_CODES = [200, 201, 204, 400, 401, 403, 404, 500, 502, 503]

def generate_log_entry():
    """Génère une entrée de log fictive"""
    log_level = random.choice(LOG_LEVELS)
    service = random.choice(SERVICES)
    
    # Génère un timestamp aléatoire dans les 7 derniers jours
    timestamp = datetime.now() - timedelta(
        days=random.randint(0, 7),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    
    log_entry = {
        '@timestamp': timestamp.isoformat(),
        'level': log_level,
        'service': service,
        'host': fake.ipv4(),
        'user_id': fake.uuid4(),
        'message': fake.sentence(),
    }
    
    # Ajoute des données spécifiques selon le service
    if service in ['api', 'web']:
        log_entry.update({
            'http_method': random.choice(HTTP_METHODS),
            'http_code': random.choice(HTTP_CODES),
            'endpoint': f"/{fake.word()}/{fake.word()}",
            'response_time': random.randint(10, 2000),
            'user_agent': fake.user_agent()
        })
    
    if service == 'database':
        log_entry.update({
            'query_type': random.choice(['SELECT', 'INSERT', 'UPDATE', 'DELETE']),
            'query_time': random.randint(1, 500),
            'rows_affected': random.randint(0, 1000)
        })
    
    # Ajoute plus de détails pour les erreurs
    if log_level == 'ERROR':
        log_entry['error_message'] = fake.sentence()
        log_entry['stack_trace'] = f"{fake.word()}.{fake.word()}: {fake.sentence()}"
    
    return log_entry

def send_to_logstash(log_entry):
    """Envoie un log à Logstash via TCP"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((LOGSTASH_HOST, LOGSTASH_PORT))
        sock.send((json.dumps(log_entry) + '\n').encode('utf-8'))
        sock.close()
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi: {e}")
        return False

def main():
    print(f"Génération de {NUM_LOGS} logs fictifs...")
    print(f"Envoi vers Logstash sur {LOGSTASH_HOST}:{LOGSTASH_PORT}")
    
    success_count = 0
    for i in range(NUM_LOGS):
        log_entry = generate_log_entry()
        
        if send_to_logstash(log_entry):
            success_count += 1
            print(f"✓ Log {i+1}/{NUM_LOGS} envoyé - {log_entry['level']} - {log_entry['service']}")
        else:
            print(f"✗ Log {i+1}/{NUM_LOGS} échoué")
        
        # Petite pause pour ne pas surcharger
        time.sleep(0.1)
    
    print(f"\n{success_count}/{NUM_LOGS} logs envoyés avec succès!")
    print(f"Accédez à Kibana sur http://localhost:5601 pour visualiser les données")

if __name__ == '__main__':
    main()