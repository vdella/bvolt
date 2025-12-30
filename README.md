# bvolt
A modular plug-and-play Microgrid Digital Twin environment for simulation, modeling and control of renewable energy resources.

## System Architecture

The BVOLT platform is organized around a strict separation between
hardware access, state persistence, and remote API exposure.

```mermaid
flowchart TB
INV["Physical Inverter (Modbus/Serial)"]
MODBUS["Modbus/Serial"]
WORKER["Polling Worker (hardware-facing)"]

INV --> MODBUS --> WORKER
WORKER -->|writes| DB["InfluxDB/State Cache"]
DB -->|reads| WORKER
DB -->|reads| API["BVOLT REST API (FastAPI)"]
API -->|writes| DB
CLIENT["Remote Client"]
CLIENT <-->|HTTP| API
```