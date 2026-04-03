# Architecture

## System Overview

TOM Demand Management System is a CLI + REST API application for portfolio prioritization at CTT. It reads CSV data, validates it, applies proportional allocation algorithms across lifecycle queues, and outputs ranked CSV results.

```mermaid
graph TB
    subgraph Interfaces
        CLI[CLI<br/>python3 tom_demand.py]
        API[REST API<br/>FastAPI]
        FE[Frontend<br/>React + Vite]
    end

    subgraph Services
        DS[DemandService]
        RDS[ReferenceDataService]
    end

    subgraph Core
        L[Loader]
        V[Validator]
        P[Prioritizer]
        E[Exporter]
    end

    subgraph Algorithms
        SL[Sainte-Laguë]
        DH[D'Hondt]
        WS[WSJF]
    end

    subgraph Storage
        CSV_IN[data/input/*.csv]
        CSV_OUT[data/output/*.csv]
        AUDIT[api_audit.jsonl]
    end

    CLI --> DS
    API --> DS
    API --> RDS
    FE --> API
    DS --> L
    L --> V
    DS --> P
    P --> E
    P --> SL
    P --> DH
    P --> WS
    CSV_IN --> L
    E --> CSV_OUT
    API --> AUDIT
```

## Data Flow

```mermaid
flowchart LR
    A["ideas.csv\nweights_*.csv"] -->|load| B[Loader]
    B -->|validate| C[Validator]
    C -->|assign queues| D[Prioritizer]
    D -->|Level 2: within RS| E[RS Ranking]
    E -->|Level 3: global| F[Global Ranking]
    F -->|export| G["demand.csv\nmetadata.json"]
```

## Queue System

IDEAs are automatically assigned to queues based on their `MicroPhase` field. Queues are ranked sequentially — highest to lowest priority:

```mermaid
flowchart TD
    INPUT[IDEA with MicroPhase] --> Q{Queue Assignment}

    Q -->|"In Development\nReady for Acceptance\nIn Acceptance\nSelected for Production"| NOW["NOW Queue\nRanks 1–N\nActive development"]
    Q -->|Ready for Development| NEXT["NEXT Queue\nRanks N+1–M\nReady to start"]
    Q -->|"Backlog · In Definition · Pitch\nReady for Solution · High Level Design\nReady for Approval · In Approval"| LATER["LATER Queue\nRanks M+1–P\nPlanning phase"]
    Q -->|"In Rollout\nIn Production"| PROD["PRODUCTION\nNo rank\nTracking only"]

    NOW --> RANK[Final Ranked List]
    NEXT --> RANK
    LATER --> RANK
    PROD -->|excluded from ranking| RANK
```

## Multi-Level Prioritization

```mermaid
flowchart LR
    L1["Level 1\nRA self-ranking\n(PriorityRA field)"]
    L2A["Level 2A\nWithin RS\nby RA weights"]
    L2B["Level 2B\nWithin RS\nby Budget Group weights"]
    L3["Level 3\nGlobal\nby RS strategic weights"]

    L1 --> L2A --> L2B --> L3 --> OUT[demand.csv]
```

## Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `src/loader.py` | Read CSVs, apply defaults, assign Queue from MicroPhase |
| `src/validator.py` | Validate IDEAS, weights, referential integrity, PriorityRA sequences |
| `src/prioritizer.py` | Orchestrate Level 2 → Level 3; dispatch to algorithms per queue |
| `src/algorithms/sainte_lague.py` | Odd-divisor proportional allocation (1, 3, 5…) |
| `src/algorithms/dhondt.py` | Natural-divisor allocation (1, 2, 3…) — reinforces dominant areas |
| `src/algorithms/wsjf.py` | (Value + Urgency + Risk) / Size, adjusted by weights |
| `src/exporter.py` | Format results, write CSVs (European format), write metadata JSON |
| `src/cli.py` | Click-based CLI — validate, prioritize, prioritize-rs, prioritize-global, compare |
| `src/services/demand_service.py` | Shared pipeline (load → validate → prioritize → export) used by CLI and API |
| `src/services/reference_data_service.py` | File-backed IDEAS and weight management for the API layer |
| `src/api/` | FastAPI app: CORS, auth, audit logging, async jobs, routers |

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| CSV as source of truth | No database dependency; files are directly manageable |
| Shared `DemandService` | Single pipeline for CLI and API — prevents logic divergence |
| `print()` not logging | Intentional for CLI UX; API layer adds structured logging separately |
| try/except import fallback | Supports both `python3 tom_demand.py` (CLI) and `from src.xxx import ...` (API) — do not restructure imports without testing both modes |
| `PriorityRA == 999` filter | Silent "disabled" flag; IDEAs with this value are excluded from prioritization |
| `Weight == 999` filter | RAs with this RA weight are excluded entirely; their IDEAs are skipped with a warning |
| Auth disabled by default | Set `AUTH_ENABLED=true` to enable API key + role authentication |
