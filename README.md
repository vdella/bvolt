# bvolt
A modular plug-and-play Microgrid Digital Twin environment for simulation, modeling and control of renewable energy resources.

## System Architecture

The BVOLT platform is organized around a strict separation between
hardware access, state persistence, and remote API exposure.

```mermaid
flowchart LR
%% =====================
%% Physical System
%% =====================
    INVERTERS["3-phase inverters"]
    EMS["EMS"]

    INVERTERS --> EMS

%% =====================
%% Hardware-facing Layer
%% =====================
    WORKER["Polling Worker (hardware-facing)"]
    EMS -->|Modbus/Serial| WORKER

%% =====================
%% State Persistence
%% =====================
    DB["InfluxDB/State Cache"]

    WORKER -->|writes| DB
    DB -->|reads| WORKER

%% =====================
%% Estimation Layer
%% =====================
    MHE["Model-Based SOC Estimator"]
    TFT["Data-Driven SOC Estimator"]

    DB --> MHE
    DB --> TFT

%% =====================
%% Benchmarking
%% =====================
    COMPARE["Benchmarking and Comparison Metrics"]

    MHE --> COMPARE
    TFT --> COMPARE

%% =====================
%% Digital Twin
%% =====================
    TWIN["Digital Twin Environment (State twinning and model parameter adjustment)"]

COMPARE --> TWIN

%% =====================
%% Visualization
%% =====================
DASH["Grafana Dashboard SOC Visualization"]

TWIN --> DASH

%% =====================
%% API Layer (BVOLT)
%% =====================
API["BVOLT REST API (FastAPI)"]

DB -->|reads| API
API -->|writes commands| DB

%% =====================
%% Remote Client
%% =====================
CLIENT["Remote Client"]

CLIENT <-->|HTTP| API

%% =====================
%% Feedback Loops (Optional)
%% =====================
TWIN -.-> MHE
TWIN -.-> TFT
```