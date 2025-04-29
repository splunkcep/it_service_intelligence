#!/usr/bin/env python3

import random
import time
from datetime import datetime

# Configuração do arquivo de saída (ou enviar para syslog)
LOG_FILE = "cisco_asa_simulated.log"  # Altere para "/var/log/cisco_asa.log" se necessário

# Dados simulados
IPS = ["10.1.2.30", "192.168.1.1", "172.16.0.5", "10.0.0.2", "192.168.100.10"]
DEST_IPS = ["192.0.0.8", "192.0.0.89", "192.0.2.10", "10.123.3.42", "192.168.33.31"]
USERS = ["user1", "user2", "admin", "test_user", "security"]
ACTIONS = ["Deny", "permit", "Teardown", "Built"]
PROTOCOLS = ["tcp", "udp", "icmp"]
LOG_LEVELS = ["%ASA-4", "%ASA-5", "%ASA-6", "%ASA-3"]

# Função para gerar um log aleatório
def generate_log():
    timestamp = datetime.now().strftime("%b %d %Y %H:%M:%S")
    log_level = random.choice(LOG_LEVELS)
    action = random.choice(ACTIONS)
    src_ip = random.choice(IPS)
    src_port = random.randint(1000, 65000)
    dst_ip = random.choice(DEST_IPS)
    dst_port = random.randint(20, 8080)
    user = random.choice(USERS)
    protocol = random.choice(PROTOCOLS)
    
    # Formato do log
    log_entry = f"{timestamp}: {log_level}-106100: access-list acl_in {action} {protocol} inside/{src_ip}({src_port}) -> outside/{dst_ip}({dst_port}) by user {user}"
    
    return log_entry

# Função principal
def main():
    print("⏳ Gerando logs do Cisco ASA a cada 5 segundos...")
    
    while True:
        log = generate_log()
        print(log)

        # Escrevendo no arquivo
        with open(LOG_FILE, "a") as file:
            file.write(log + "\n")

        time.sleep(5)

if __name__ == "__main__":
    main()
