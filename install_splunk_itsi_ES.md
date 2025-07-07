# Guía de Prueba de Concepto (POC) de ITSI - Splunk

## Resumen
Este repositorio ofrece una guía paso a paso para que los socios de Splunk aprendan a configurar y demostrar una POC de Inteligencia de Servicios de TI (ITSI). El objetivo es crear un entorno funcional para la monitorización, la correlación de eventos y la detección de anomalías.

## Fases del Proyecto

1. Instalar la arquitectura S1 de Splunk.
2. Instalar ITSI y obtener la licencia.
3. Ingerir datos.
4. Crear el árbol de servicios.

## Enlaces de referencia

Para garantizar una instalación y configuración correctas, consulte los siguientes enlaces:

- [Documentación oficial de Splunk Enterprise](https://docs.splunk.com/Documentation/Splunk)
- [Guía de instalación de ITSI](https://docs.splunk.com/Documentation/ITSI)
- [Descarga de Splunk](https://www.splunk.com/en_us/download.html)
- [Requisitos de ITSI](https://docs.splunk.com/Documentation/ITSI/latest/Install/DeploymentPlanning)
- [Administración del firewall para Splunk](https://docs.splunk.com/Documentation/Splunk/latest/Admin/Networkports)

## Detalles de las dependencias

Antes de comenzar la instalación, asegúrese de que los siguientes paquetes estén instalados:

```bash
sudo yum install -y wget curl tar unzip firewalld
```

Si usa Ubuntu/Debian, use:

```bash
sudo apt update && sudo apt install -y wget curl tar unzip firewalld
```

Asegúrese de que `firewalld` esté habilitado:

```bash
sudo systemctl enable firewalld --now
```

### 1. Instalación de Splunk (Arquitectura S1)
#### Requisitos de hardware y software

Antes de comenzar la instalación de Splunk, es fundamental asegurarse de que el entorno cumpla con los requisitos mínimos de hardware y software según la documentación oficial de Splunk ITSI ([Referencia](https://docs.splunk.com/Documentation/ITSI/4.20.0/Install/Plan)).

##### Hardware recomendado:
| Componente | Requisitos mínimos |
|----------------|------------------|
| CPU | 24 vCPU |
| RAM | 12 GB |
| Almacenamiento | SSD de 100 GB |
| Red | Ethernet de 1 Gbps |

##### Software recomendado:
| Componente | Versión requerida |
|--------------|----------------|
| Sistema operativo | Linux (Ubuntu 20.04+, CentOS 7+, RHEL 8+) |
| Paquetes adicionales | `wget`, `curl`, `tar`, `unzip`, `firewalld` (si corresponde) |

#### Dependencias de red:
Asegúrese de que los siguientes puertos estén abiertos:
| Servicio | Puerto |
|--------------|------|
| Interfaz web (HTTPS) | 8000 |
| Indexación | 9997 |
| Reenvío | 8089 |
| Servidor de implementación | 8089 |
| HEC | 8088 |
| KV Store | 8191 |

---
### 2. Instalación y licencia de ITSI
#### Requisitos de la prueba de concepto (POC) de ITSI
Para realizar una POC de ITSI, se deben cumplir los siguientes criterios:
- Una **oportunidad disponible** en Splunk.
- La POC debe ser aprobada como viable por el departamento de ventas de Splunk.
- Las licencias solo estarán disponibles **tras la aprobación** de la POC.

#### Descarga e instalación de ITSI
ITSI se puede descargar de las siguientes maneras:
- Directamente desde [Splunkbase](https://splunkbase.splunk.com/app/1841) (si existe una licencia válida para la cuenta de Splunk asociada).
- Mediante solicitud al equipo de **Ingenieros de soluciones (SE) de Splunk** o **Ingenieros de soluciones para socios (PSE) de Splunk**, si la POC ha sido aprobada.

#### Solicitud de licencia
Tras recibir la licencia de ITSI:
1. Acceda a Splunk Web a través del navegador web. 2. Inicia sesión con las credenciales:
- **Usuario**: `admin`
- **Contraseña**: `splunkuser`
3. Ve a **Configuración > Licencias**.
4. Haz clic en **Añadir licencia** y sube el archivo `license.lic`.
5. Confirma la activación de la licencia.

#### Configuración inicial de ITSI
ITSI **no se puede instalar a través de Splunk Web**; debe extraerse manualmente a la carpeta correcta.

### **Pasos para instalar ITSI mediante CLI**

1️⃣ **Asegúrese de que el archivo ITSI (`.spl`) esté en el directorio correcto y tenga permisos de ejecución**:
```bash
ls -lha /home/splunkuser/splunk-it-service-intelligence_4200.spl
```
Si el archivo no está disponible, descárguelo según las instrucciones anteriores. Para configurar los permisos de ejecución:

```bash
sudo chmod +x /home/splunkuser/splunk-it-service-intelligence_4200.spl
```

2️⃣ **Extraiga ITSI a la carpeta de aplicaciones de Splunk**:
```bash
sudo -u splunkuser tar -xvf /home/splunkuser/splunk-it-service-intelligence_4200.spl -C /opt/splunk/etc/apps/
```

3️⃣ **Corrija los permisos para que Splunk pueda acceder a él correctamente**:
```bash
sudo chown -R splunkuser:splunkuser /opt/splunk/etc/apps/itsi
```

4️⃣ **Reinicie Splunk para aplicar la instalación**:
```bash
sudo -u splunkuser /opt/splunk/bin/splunk restart
```

5️⃣ **Tras reiniciar, acceda a ITSI en Splunk Web**:
- Vaya a **Aplicaciones > IT Service Intelligence** para completar la configuración inicial.

##### Configuración detallada
1. **Configuración de índices:**
- Vaya a **Configuración > Índices** y cree los siguientes índices si aún no existen:
- `itsi_summary`
- `itsi_tracked_alerts`
- `itsi_notable_grouped_events`
- Asegúrese de que haya suficiente espacio en disco para almacenar los eventos.

2. **Configuración de permisos de usuario:**
- Vaya a **Configuración > Controles de acceso > Roles**.
- Cree o modifique roles para garantizar que los usuarios relevantes tengan permisos para ver y administrar ITSI. - Agregue los usuarios correctos al grupo: un nuevo usuario llamado `analyst` a `itoa_admin` y otro llamado `user` asociado a `itoa_user`.
- No es necesario marcar la opción "Requerir cambio de contraseña en el próximo inicio de sesión".
- Use la misma contraseña para facilitar el laboratorio.

3. **Inicio de KV Store:**
- Ejecute el siguiente comando para comprobar el estado de KV Store:
```bash
sudo -u splunkuser /opt/splunk/bin/splunk show kvstore-status
```
- El usuario `admin` y la misma contraseña compartida anteriormente.

- Si es necesario, reinicie el almacén KV:
```bash
sudo -u splunkuser /opt/splunk/bin/splunk restart splunkd
```
## **Estructura del árbol de servicios**
La prueba de concepto (POC) se basará en una aplicación monolítica, donde cada servicio representa un componente esencial del sistema:

### **Servicios e indicadores clave de rendimiento (KPI)**
1. **Interfaz web**
- **KPI:**
- Uso de CPU
- Latencia de red
- **Dependencia:** API de backend

2. **API de backend**
- **KPI:**
- Uso de CPU
- Latencia de red
- **Dependencia:** Servicio de base de datos y autenticación

3. **Base de datos**
- **KPI:**
- Uso de CPU
- Latencia de red
- **Dependencia:** Almacenamiento

4. **Servicio de autenticación**
- **KPI:**
- Uso de CPU
- Red Latencia
- **Dependencia:** Base de datos

5. **Almacenamiento**
- **KPI:**
- Uso de disco
- Latencia de lectura/escritura
- Espacio disponible
- **Dependencia:** Ninguna (basada en la infraestructura)
-
---

### **1. Crear servicios en ITSI (sin dependencias)**
Los servicios deben crearse **inicialmente sin dependencias**. La vinculación se realizará posteriormente, en **Service Analyzer**.

1. Acceda a **ITSI > Asistente de configuración**.
2. Vaya a **Configuración del servicio > Configurar servicios**.
3. Crear servicio > Crear servicio. Cree los servicios:

* Título: Almacenamiento | * Título: Servicio de autenticación | * Título: Base de datos | * Título: API de backend | * Título: Servicios e indicadores clave de rendimiento (KPI)
* Agregar manualmente el contenido del servicio

KPI

Para cada servicio anterior, vaya a la pestaña KPI > Nuevo > KPI genérico
* Título: Uso de CPU de almacenamiento

Búsqueda ad hoc
```
| makeresults count=100
| streamstats count as time
| eval CPU_Usage=round(random()%100,2)
```
Campo Umbral: CPU_Usage

Programación de búsqueda de KPI: Cada minuto

Unidad: %

Configure los **umbrales** en:
Crítico: 80
Alto: 70
Medio: 50
Bajo: 40

Para cada servicio anterior, vaya a la pestaña KPI > Nuevo > KPI genérico
* Título: Latencia de red

Búsqueda ad hoc
```
| makeresults count=100
| streamstats count as time
| eval Latency=round(random()%500,2)
```
Campo Umbral: Latencia

Programación de búsqueda de KPI: Cada minuto

Unidad: ms

Establezca los **umbrales** en:
Crítico: 50
Alto: 40
Medio: 30
Bajo: 20

### **Configurar el árbol de dependencias en el Analizador de Servicios**
Las dependencias se pueden configurar al crear el servicio o posteriormente. En este caso, lo haremos más adelante. Revisemos cada servicio creado y vayamos a la pestaña Dependencias del Servicio y luego a Agregar dependencias:

1. Acceda a **ITSI > Asistente de Configuración**.
2. Vaya a **Configuración del Servicio > Almacenamiento, Servicio de Autenticación, etc.**.
3. Pestaña Dependencias del Servicio > Para cada servicio, siga estos pasos:

Seleccione "Uso de CPU", Simulación de Latencia de Red y ServiceHealthScore:

• El frontend web depende de la API del backend. • La API de backend depende del servicio de autenticación y de la base de datos.
• La base de datos depende del almacenamiento.
• El almacenamiento es la base de la infraestructura.

Vayamos al Analizador de Servicios para ver cómo se ven las métricas.

Ahora haga clic en la Vista de árbol.

Tómese unos minutos para explorar las métricas y el árbol de servicios.

Próximos pasos para configurar una alarma en ITSI

El objetivo es crear una alarma basada en los KPI simulados, que se agruparán en episodios (Vista de episodios) en ITSI.

⸻

1️⃣ Crear una condición de activación en un KPI
1. Vaya a ITSI > Configuración > Servicios.
2. Seleccione uno de los servicios creados (por ejemplo, API de backend).
3. Vaya a la pestaña KPI y elija un KPI (por ejemplo, Uso de CPU).
4. Haga clic en Editar KPI y desplácese hacia abajo hasta Condiciones de activación. 5. Agregue un nuevo disparador:
• Nombre: Alerta de CPU alta
• Condición: Si el uso de CPU es > 80 %, se genera un evento notable.
• Gravedad: Crítica
6. Guarde la configuración.

⸻

2️⃣ Cree una Política de Agregación de Eventos Notables (NEAP)

Ahora debemos asegurarnos de que los eventos generados por los KPI se agrupen correctamente en episodios.
1. Vaya a ITSI > Configuración > Gestión de eventos > Políticas de agregación.
2. Haga clic en Nueva política de agregación.
3. Complete los detalles:
• Nombre: Alerta de CPU alta
• Descripción: Política para agrupar alertas de CPU alta.
• Reglas de entidad: Agregue una regla para agrupar por entidad (por ejemplo, host).
4. Vaya a Condiciones de disparo y agregue:
• Si la gravedad es crítica, cree un evento notable.
5. Elija un grupo de eventos para esta alarma (por ejemplo, Alertas de infraestructura).
6. Haga clic en Guardar. ⸻

3️⃣ Consulta los episodios creados
1. Ve a ITSI > Alertas y episodios.
2. Verás cómo se crean los episodios a medida que se generan las alertas.
3. Si quieres ver los detalles, haz clic en el episodio para ver los eventos destacados agregados.

⸻

4️⃣ (Opcional) Configurar una acción automática

Podemos configurar una acción automática, como una notificación por correo electrónico o un script.
1. Dentro de la Política de agregación, ve a Acciones.
2. Elige una acción, como Enviar correo electrónico o Ejecutar script.
3. Configura los parámetros necesarios.
4. Guarda y prueba la alarma.
