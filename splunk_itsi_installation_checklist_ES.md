# Splunk ITSI - Lista de verificación de instalación y configuración

## 1. Objetivo

Este documento proporciona una lista de verificación detallada para implementar **Splunk IT Service Intelligence (ITSI)**, que incluye todas las configuraciones, casos de uso, KPI, árboles de servicios, dependencias y complementos necesarios.

---

## 2. Requisitos previos

- **Versión de Splunk Enterprise**: ≥ 8.2.x
- **Versión de ITSI**: ≥ 4.15
- **Compatibilidad con clúster de búsqueda principal** (opcional)
- **Licencia**: Asegúrese de tener instalada una licencia válida de ITSI
- **Sincronización horaria**: NTP configurado en todos los componentes
- **Indexación**: Utilice índices dedicados (p. ej., `itsi_summary`, `itsi_tracked_alerts`, `itsi_notable_events`)

---

## 3. Componentes principales de ITSI

- **Búsquedas base de KPI** (búsquedas guardadas programadas)
- **KPI** (KPI = búsqueda base + umbrales + agregación)
- **Servicios** (agrupación de KPI para modelar unidades de negocio/infraestructura)
- **Árboles de servicios** (asignación de dependencias)
- **Tablas de Glass** (visualización en tiempo real) Paneles de control)
- **Eventos notables** (usados ​​en búsquedas de correlación y episodios)
- **Revisión de episodios** (clasificación de alertas mediante el motor de correlación)
- **Entradas modulares** (importación de datos de KPI o fuentes de métricas externas)

---

## 4. Complementos y entradas

| Tipo de entrada | Complemento requerido | Referencia del modelo de datos |
|---------------------|----------------------------------------|----------------------------|
| Métricas del SO (Linux) | Splunk_TA_nix | Rendimiento, disponibilidad |
| Métricas del SO (Windows) | Splunk_TA_windows | Rendimiento, disponibilidad |
| VMware | Splunk_TA_vmware | Computación, virtualización |
| Red | Transmisión, Cisco TA, entrada modular SNMP | Tráfico de red |
| Registros | Cisco ASA, Fortinet, Syslog, JournalD | Varía según la fuente del KPI |
| APM/Infra Cloud | Integración de Splunk Observability | Métricas en tiempo real |

---

## 5. KPI por servicio (Ejemplo de árbol)

| Servicio | KPI incluidos | Campos/Fuente obligatorios |
|----------------------------|------------------------------------------|------------------------------------------------|
| Aplicación: API de servicio de IA | Uso de CPU, Uso de memoria, Errores HTTP | `host`, `cpu_idle`, `mem_used_percent`, `status` |
| Backend: Motor de modelos | Tamaño de la cola de trabajos, Trabajos fallidos, E/S de disco | `queue_size`, `failed_jobs`, `disk_read/write` |
| Infraestructura: Clúster Linux | CPU, RAM, Disco | `host`, `cpu`, `memory`, `disk` |
| Proxy/Puerta de enlace API | Latencia, Errores, Solicitudes por segundo | `uri`, `status`, `latency`, `count` | | Base de datos | QPS, Consultas lentas, Estado de replicación | `query_count`, `slow_queries`, `replica_status` |

---

## 6. Lista de verificación de configuración

### Configuración de ITSI

- [x] ITSI instalado y con licencia
- [x] Roles de ITSI (`itsi_admin`, `itsi_user`) asignados
- [x] Índice `itsi_summary` configurado
- [x] Plantilla de servicio predeterminada de ITSI aplicada

### Búsquedas base de KPI

- [x] Búsquedas guardadas creadas y visibles
- [x] Agregación (promedio, porcentaje, suma) establecida
- [x] Aceleración habilitada si es necesario

### KPI

- [x] Creado con los umbrales correctos
- [x] Vinculado a servicios
- [x] Plantillas de umbral aplicadas (p. ej., estáticas, adaptativas)

### Servicios

- [x] Todos los componentes principales modelados como servicios
- [x] Árbol de dependencias definido
- [x] Subservicios anidados si corresponde

### Eventos notables

- [x] Alertas de umbral convertidas en Notables
- [x] Reglas de correlación creadas (reglas de episodio)

### Tablas de Glass

- [x] Visualizaciones de estado y KPI en tiempo real
- [x] Vinculación con KPI en tiempo real
- [x] Indicadores visuales personalizados añadidos (SVG, iconos)

---

## 7. Validación posterior a la instalación

- [x] Comprobar que el índice `itsi_summary` se esté rellenando
- [x] Validar la integridad y las dependencias del árbol de servicios
- [x] Validar las búsquedas de base y los valores de KPI
- [x] Revisar las tablas de Glass y asegurarse de que no falten datos
- [x] Comprobar la correcta correlación de alertas en la revisión de episodios

---

## 8. Mejoras opcionales

- Integrar las métricas de **Splunk Observability Cloud**
- Usar **External Service Insights (ESI)** para enriquecer los datos
- Crear análisis predictivos con **ITSI Machine Learning Toolkit**
- Usar **Anomaly Detection** como referencia Desviaciones
- Importar métricas personalizadas mediante el Recopilador de Eventos REST/HTTP (HEC)

---

## 9. Automatización y Simulación

- Usar `makeresults` para simulaciones de laboratorio (SPL)
- Simular KPI con búsquedas programadas
- Crear automáticamente servicios/KPI mediante la API REST o archivos de configuración
