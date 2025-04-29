# Guia para POC de ITSI - Splunk

## Visão Geral
Este repositório tem como objetivo fornecer um guia passo a passo para que parceiros Splunk possam aprender a configurar e demonstrar uma POC do IT Service Intelligence (ITSI). O foco é criar um ambiente funcional para monitoramento, correlação de eventos e detecção de anomalias.

## Fases do Projeto

1. Instalação do Splunk arquitetura S1.
2. Instalação do ITSI e licenciamento.
3. Ingestão de dados.
4. Criação de árvore de serviço.

## Links de Referência

Para garantir uma instalação e configuração corretas, consulte os seguintes links:

- [Documentação Oficial do Splunk Enterprise](https://docs.splunk.com/Documentation/Splunk)
- [Guia de Instalação do ITSI](https://docs.splunk.com/Documentation/ITSI)
- [Download do Splunk](https://www.splunk.com/en_us/download.html)
- [Requisitos do ITSI](https://docs.splunk.com/Documentation/ITSI/latest/Install/DeploymentPlanning)
- [Administração de Firewalls para Splunk](https://docs.splunk.com/Documentation/Splunk/latest/Admin/Networkports)

## Detalhamento das Dependências

Antes de iniciar a instalação, certifique-se de que os seguintes pacotes estão instalados:

```bash
sudo yum install -y wget curl tar unzip firewalld
```

Caso esteja utilizando Ubuntu/Debian, use:

```bash
sudo apt update && sudo apt install -y wget curl tar unzip firewalld
```

Certifique-se de que o `firewalld` está ativo:

```bash
sudo systemctl enable firewalld --now
```

### 1. Instalação do Splunk (Arquitetura S1)
#### Requisitos de Hardware e Software

Antes de iniciar a instalação do Splunk, é essencial garantir que o ambiente atenda aos requisitos mínimos de hardware e software conforme a documentação oficial do Splunk ITSI ([Referência](https://docs.splunk.com/Documentation/ITSI/4.20.0/Install/Plan)).

##### Hardware Recomendado:
| Componente      | Requisitos Mínimos |
|----------------|------------------|
| CPU           | 24 vCPUs          |
| Memória RAM   | 12 GB             |
| Armazenamento | 100 GB SSD        |
| Rede         | 1 Gbps Ethernet    |

##### Software Recomendado:
| Componente    | Versão Requerida |
|--------------|----------------|
| SO          | Linux (Ubuntu 20.04+, CentOS 7+, RHEL 8+) |
| Pacotes adicionais | `wget`, `curl`, `tar`, `unzip`, `firewalld` (se aplicável) |

##### Dependências de Rede:
Certifique-se de que as seguintes portas estão abertas:
| Serviço       | Porta |
|--------------|------|
| Web UI (HTTPS) | 8000 |
| Indexação | 9997 |
| Forwarding | 8089 |
| Deployment Server | 8089 |
| HEC | 8088 |
| KV Store | 8191 |

---

### 2. Instalação do ITSI e Licenciamento
#### Requisitos para POC do ITSI
Para realizar uma POC de ITSI, é necessário atender aos seguintes critérios:
- Uma **oportunidade aberta** na Splunk.
- A POC precisa ser aprovada como exequível pela equipe de vendas da Splunk.
- O licenciamento será disponibilizado **apenas após a aprovação** da POC.

#### Download e Instalação do ITSI
O ITSI pode ser baixado das seguintes formas:
- Diretamente pelo [Splunkbase](https://splunkbase.splunk.com/app/1841) (se houver uma licença válida para a conta Splunk associada).
- Mediante solicitação à equipe **Splunk Solutions Engineer (SE)** ou **Splunk Partner Solutions Engineer (PSE)**, caso a POC tenha sido aprovada.

#### Aplicação da Licença
Após receber a licença de ITSI:
1. Acesse o Splunk Web via navegador.
2. Faça login com as credenciais:
   - **Usuário**: `admin`
   - **Senha**: `splunkuser`
3. Navegue até **Settings > Licensing**.
4. Clique em **Add license** e faça o upload do arquivo `license.lic`.
5. Confirme a ativação da licença.

#### Configuração Inicial do ITSI
O ITSI **não pode ser instalado via Splunk Web**, ele deve ser extraído manualmente na pasta correta.

### **Passos para instalar o ITSI via CLI**

1️⃣ **Certifique-se de que o arquivo ITSI (`.spl`) está no diretório correto e sua permissão de execução**:
   ```bash
   ls -lha /home/splunkuser/splunk-it-service-intelligence_4200.spl
   ```
   Se o arquivo não estiver lá, faça o download conforme orientações anteriores. Para colocar permissão de execução:

   ```bash
   sudo chmod +x /home/splunkuser/splunk-it-service-intelligence_4200.spl
   ```

2️⃣ **Extraia o ITSI na pasta de aplicativos do Splunk**:
   ```bash
   sudo -u splunkuser tar -xvf /home/splunkuser/splunk-it-service-intelligence_4200.spl -C /opt/splunk/etc/apps/
   ```

3️⃣ **Corrija as permissões para o Splunk acessar corretamente**:
   ```bash
   sudo chown -R splunkuser:splunkuser /opt/splunk/etc/apps/itsi
   ```

4️⃣ **Reinicie o Splunk para aplicar a instalação**:
   ```bash
   sudo -u splunkuser /opt/splunk/bin/splunk restart
   ```

5️⃣ **Após a reinicialização, acesse o ITSI no Splunk Web**:
   - Navegue até **Apps > IT Service Intelligence** para concluir a configuração inicial.

##### Configuração Detalhada
1. **Configuração de Índices:**
   - Vá para **Settings > Indexes** e crie os seguintes índices se ainda não existirem:
     - `itsi_summary`
     - `itsi_tracked_alerts`
     - `itsi_notable_grouped_events`
   - Verifique se há espaço suficiente em disco para a retenção dos eventos.

2. **Definição de Permissões de Usuários:**
   - Acesse **Settings > Access Controls > Roles**.
   - Crie ou modifique os papéis para garantir que usuários relevantes tenham permissões para visualizar e gerenciar o ITSI.
   - Adicione os usuários corretos ao grupo, um novo usuario chamado `analyst` ao `itoa_admin` e outro chamado `user` associado ao `itoa_user`.
   - `Não` precisa marcar a opção "Require password change on next login".
   - Use a mesma senha para facilitar o laboratório.

3. **Inicialização do KV Store:**
   - Execute o seguinte comando para verificar o status do KV Store:
     ```bash
     sudo -u splunkuser /opt/splunk/bin/splunk show kvstore-status
     ```
   - Usuário admin e a mesma senha compatilhada anteriormente.
     
   - Se necessário, reinicie o KV Store:
     ```bash
     sudo -u splunkuser /opt/splunk/bin/splunk restart splunkd
     ```
## **Estrutura da Árvore de Serviços**
A POC será baseada em uma aplicação monolítica, onde cada serviço representa um componente essencial do sistema:

### **Serviços e KPIs**
1. **Frontend Web**
   - **KPIs:**
     - CPU Usage
     - Latência de Rede
   - **Dependência:** Backend API

2. **Backend API**
   - **KPIs:**
     - CPU Usage
     - Latência de Rede
   - **Dependência:** Database & Authentication Service

3. **Database**
   - **KPIs:**
     - CPU Usage
     - Latência de Rede
   - **Dependência:** Storage

4. **Authentication Service**
   - **KPIs:**
     - CPU Usage
     - Latência de Rede
   - **Dependência:** Database

5. **Storage**
   - **KPIs:**
     - Disk Usage
     - Read/Write Latency
     - Available Space
   - **Dependência:** Nenhuma (base da infraestrutura)
   - 
---

### **1. Criar os Serviços no ITSI (Sem Dependências)**
Os serviços devem ser criados **sem dependências inicialmente**. A vinculação será feita depois, dentro do **Service Analyzer**.

1. Acesse **ITSI > Configuration Assistant**.
2. Vá para **Service Configuration > Configure Services**.
3. Create Service > Create Service. Crie os serviços:

* Title: Storage | * Title: Authentication Service | * Title: Database | * Title: Backend API | * Title: Serviços e KPIs
* Manually add service content
  
KPIs

Para cada serviço acima. Vá na guia KPIs > New > Generic KPI
* Title: Storage CPU_Usage

Ad hoc Search
```
| makeresults count=100 
| streamstats count as time 
| eval CPU_Usage=round(random()%100,2)
```
Threshold Field: CPU_Usage

KPI Search Schedule: Every minute

Unit: %

Configure os **thresholds** para:
   Critical: 80
   Hight: 70
   Medium: 50
   Low: 40

Para cada serviço acima. Vá na guia KPIs > New > Generic KPI
* Title: Network Latency
  
Ad hoc Search
```
| makeresults count=100 
| streamstats count as time 
| eval Latency=round(random()%500,2)
```
Threshold Field: Latency

KPI Search Schedule: Every minute

Unit: ms

Configure os **thresholds** para:
   Critical: 50
   Hight: 40
   Medium: 30
   Low: 20

### ** Configurar a Árvore de Dependências no Service Analyzer**
A configuração das dependências pode ser feita na criação do serviço ou posteriormente. Neste caso vamos fazer posteriormente. Vamos visitar cada serviço criado e ir até a guia Service Dependencies e depois Add dependecies:

1. Acesse **ITSI > Configuration Assistant**.
2. Vá para **Service Configuration > Storage, Authentication Service, etc**.
3. Tab Service Dependecies > Para cada serviço faça esta lógica:

Selecionar "CPU Usage", Simulação de Latência de Rede e ServiceHealthScore:

   •	O Frontend Web depende do Backend API.
	•	O Backend API depende do Authentication Service e do Database.
	•	O Database depende do Storage.
	•	O Storage é a base da infraestrutura.

 Vamos até o Service Analyzer olhar como ficou as metricas.

 Agora clique no Tree View. 

 Tome alguns minutos para explorar as metricas e arvore de serviços.

 Próximos Passos para Configurar um Alarme no ITSI

O objetivo é criar um alarme baseado nos KPIs simulados, que será agrupado nos Episódios (Episodes View) no ITSI.

⸻

1️⃣ Criar um Trigger Condition em um KPI
	1.	Vá para ITSI > Configuration > Services.
	2.	Selecione um dos serviços criados (exemplo: Backend API).
	3.	Vá para a aba KPIs e escolha um KPI (exemplo: CPU Usage).
	4.	Clique em Edit KPI e role até Trigger Conditions.
	5.	Adicione um novo trigger:
	•	Nome: Alerta CPU Alta
	•	Condição: Se CPU_Usage > 80% então gera um evento notável.
	•	Gravidade: Critical
	6.	Salve as configurações.

⸻

2️⃣ Criar um Notable Event Aggregation Policy (NEAP)

Agora precisamos garantir que os eventos gerados pelos KPIs sejam agrupados corretamente nos Episódios.
	1.	Vá para ITSI > Configuration > Event Management > Aggregation Policies.
	2.	Clique em New Aggregation Policy.
	3.	Preencha os detalhes:
	•	Nome: Alerta CPU Alta
	•	Description: Política para agrupar alertas de CPU alta.
	•	Entity Rules: Adicione uma regra para agrupar por entidade (exemplo: host).
	4.	Vá até Trigger Conditions e adicione:
	•	IF severity = Critical THEN create notable event.
	5.	Escolha um grupo de eventos para esse alarme (exemplo: Infrastructure Alerts).
	6.	Clique em Save.

⸻

3️⃣ Verificar os Episódios Criados
	1.	Vá para ITSI > Alerts and Episodes.
	2.	Você verá os episódios sendo criados conforme os alertas são gerados.
	3.	Se quiser visualizar detalhes, clique no episódio e veja os eventos notáveis agregados.

⸻

4️⃣ (Opcional) Configurar uma Ação Automática

Podemos configurar uma ação automática, como notificação por email ou script.
	1.	Dentro da Aggregation Policy, vá até Actions.
	2.	Escolha uma ação, como Send Email ou Run Script.
	3.	Configure os parâmetros necessários.
	4.	Salve e teste o alarme.
