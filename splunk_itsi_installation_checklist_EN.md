# Splunk ITSI - Installation & Configuration Checklist

## 1. Objective

This document provides a detailed checklist to implement **Splunk IT Service Intelligence (ITSI)** including all required configurations, use cases, KPIs, service trees, dependencies, and add-ons.

---

## 2. Prerequisites

- **Splunk Enterprise Version**: ≥ 8.2.x
- **ITSI Version**: ≥ 4.15
- **Search Head Cluster Supported** (optional)
- **License**: Ensure valid ITSI license is installed
- **Time Synchronization**: NTP configured across all components
- **Indexing**: Use dedicated indexes (e.g., `itsi_summary`, `itsi_tracked_alerts`, `itsi_notable_events`)

---

## 3. Core ITSI Components

- **KPI Base Searches** (scheduled saved searches)
- **KPIs** (KPI = base search + thresholds + aggregation)
- **Services** (group KPIs to model business/infra units)
- **Service Trees** (map dependencies)
- **Glass Tables** (real-time visual dashboards)
- **Notable Events** (used in correlation searches & episodes)
- **Episode Review** (alert triage via correlation engine)
- **Modular Inputs** (KPI data import or external metric feeds)

---

## 4. Add-ons & Inputs

| Input Type          | Add-on Required                        | Data Model Reference       |
|---------------------|----------------------------------------|----------------------------|
| OS Metrics (Linux)  | Splunk_TA_nix                          | Performance, Availability  |
| OS Metrics (Windows)| Splunk_TA_windows                      | Performance, Availability  |
| VMware              | Splunk_TA_vmware                       | Compute, Virtualization    |
| Network             | Stream, Cisco TA, SNMP Modular Input   | Network Traffic            |
| Logs                | Cisco ASA, Fortinet, Syslog, JournalD  | Varies by KPI source       |
| APM/Infra Cloud     | Splunk Observability Integration       | Real-time metrics          |

---

## 5. KPIs by Service (Example Tree)

| Service                    | KPIs Included                           | Fields/Source Required                        |
|----------------------------|------------------------------------------|------------------------------------------------|
| App: AI Service API        | CPU Usage, Memory Usage, HTTP Errors    | `host`, `cpu_idle`, `mem_used_percent`, `status` |
| Backend: Model Engine      | Job Queue Size, Failed Jobs, Disk I/O   | `queue_size`, `failed_jobs`, `disk_read/write`  |
| Infra: Linux Cluster       | CPU, RAM, Disk                          | `host`, `cpu`, `memory`, `disk`                 |
| Proxy/API Gateway          | Latency, Errors, Requests per Second    | `uri`, `status`, `latency`, `count`             |
| Database                   | QPS, Slow Queries, Replication Status   | `query_count`, `slow_queries`, `replica_status` |

---

## 6. Configuration Checklist

### ITSI Setup

- [x] ITSI Installed and licensed
- [x] ITSI roles (`itsi_admin`, `itsi_user`) assigned
- [x] `itsi_summary` index configured
- [x] ITSI Default Service Template applied

### KPI Base Searches

- [x] Savedsearches created and visible
- [x] Aggregation (avg, pct, sum) set
- [x] Acceleration enabled if necessary

### KPIs

- [x] Created with correct thresholds
- [x] Linked to services
- [x] Threshold templates applied (e.g., static, adaptive)

### Services

- [x] All major components modeled as services
- [x] Dependency tree defined
- [x] Sub-services nested if applicable

### Notable Events

- [x] Threshold alerts converted to Notables
- [x] Correlation rules created (Episode rules)

### Glass Tables

- [x] Real-time health and KPI visualizations
- [x] Linked to live KPIs
- [x] Custom visual indicators added (SVG, icons)

---

## 7. Post-Installation Validation

- [x] Check `itsi_summary` index is populating
- [x] Validate service tree for integrity and dependencies
- [x] Validate base searches and KPI values
- [x] Review glass tables and ensure no missing data
- [x] Check Episode Review for correct alert correlation

---

## 8. Optional Enhancements

- Integrate **Splunk Observability Cloud** metrics
- Use **External Service Insights (ESI)** to enrich data
- Build predictive analytics with **ITSI Machine Learning Toolkit**
- Use **Anomaly Detection** for baseline deviations
- Import custom metrics via REST/HTTP Event Collector (HEC)

---

## 9. Automation & Simulation

- Use `makeresults` for lab simulations (SPL)
- Simulate KPIs with scheduled searches
- Automatically create services/KPIs via REST API or config files
