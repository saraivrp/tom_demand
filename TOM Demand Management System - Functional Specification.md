  
  
# TOM Demand Management System - Functional Specification
## Document Information
**Document**: TOM Demand Management System - Functional Specification
**Version**: 3.1
**Date**: January 04, 2026
**Author**: Lean Portfolio Management Specialist
**Status**: Final - Approved for Implementation
**Change Log**: v3.1 - Added Queue-Based Sequential Prioritization (NOW/NEXT/PRODUCTION)  
  
## Table of Contents  
1. ++[System Overview](https://claude.ai/chat/c7c29ce8-e8f6-400e-8429-1ad7d1c89a63?setup_intent=seti_1Sl8nIBjIQrRQnuxmM5MY7td&setup_intent_client_secret=seti_1Sl8nIBjIQrRQnuxmM5MY7td_secret_TiZx3ISyMFXuJfMv4rVKfhHXmT8O1nV&source_type=card#1-system-overview)++  
2. ++[Target Operating Model (TOM) Structure](https://claude.ai/chat/c7c29ce8-e8f6-400e-8429-1ad7d1c89a63?setup_intent=seti_1Sl8nIBjIQrRQnuxmM5MY7td&setup_intent_client_secret=seti_1Sl8nIBjIQrRQnuxmM5MY7td_secret_TiZx3ISyMFXuJfMv4rVKfhHXmT8O1nV&source_type=card#2-target-operating-model-tom-structure)++  
3. ++[Data Model](https://claude.ai/chat/c7c29ce8-e8f6-400e-8429-1ad7d1c89a63?setup_intent=seti_1Sl8nIBjIQrRQnuxmM5MY7td&setup_intent_client_secret=seti_1Sl8nIBjIQrRQnuxmM5MY7td_secret_TiZx3ISyMFXuJfMv4rVKfhHXmT8O1nV&source_type=card#3-data-model)++  
4. ++[Prioritization Methods](https://claude.ai/chat/c7c29ce8-e8f6-400e-8429-1ad7d1c89a63?setup_intent=seti_1Sl8nIBjIQrRQnuxmM5MY7td&setup_intent_client_secret=seti_1Sl8nIBjIQrRQnuxmM5MY7td_secret_TiZx3ISyMFXuJfMv4rVKfhHXmT8O1nV&source_type=card#4-prioritization-methods)++  
5. ++[Prioritization Levels](https://claude.ai/chat/c7c29ce8-e8f6-400e-8429-1ad7d1c89a63?setup_intent=seti_1Sl8nIBjIQrRQnuxmM5MY7td&setup_intent_client_secret=seti_1Sl8nIBjIQrRQnuxmM5MY7td_secret_TiZx3ISyMFXuJfMv4rVKfhHXmT8O1nV&source_type=card#5-prioritization-levels)++  
6. ++[Functional Specification](https://claude.ai/chat/c7c29ce8-e8f6-400e-8429-1ad7d1c89a63?setup_intent=seti_1Sl8nIBjIQrRQnuxmM5MY7td&setup_intent_client_secret=seti_1Sl8nIBjIQrRQnuxmM5MY7td_secret_TiZx3ISyMFXuJfMv4rVKfhHXmT8O1nV&source_type=card#6-functional-specification)++  
7. ++[Use Cases and Examples](https://claude.ai/chat/c7c29ce8-e8f6-400e-8429-1ad7d1c89a63?setup_intent=seti_1Sl8nIBjIQrRQnuxmM5MY7td&setup_intent_client_secret=seti_1Sl8nIBjIQrRQnuxmM5MY7td_secret_TiZx3ISyMFXuJfMv4rVKfhHXmT8O1nV&source_type=card#7-use-cases-and-examples)++  
8. ++[Integration with TOM Delivery Model](https://claude.ai/chat/c7c29ce8-e8f6-400e-8429-1ad7d1c89a63?setup_intent=seti_1Sl8nIBjIQrRQnuxmM5MY7td&setup_intent_client_secret=seti_1Sl8nIBjIQrRQnuxmM5MY7td_secret_TiZx3ISyMFXuJfMv4rVKfhHXmT8O1nV&source_type=card#8-integration-with-tom-delivery-model)++  
9. ++[Non-Functional Requirements](https://claude.ai/chat/c7c29ce8-e8f6-400e-8429-1ad7d1c89a63?setup_intent=seti_1Sl8nIBjIQrRQnuxmM5MY7td&setup_intent_client_secret=seti_1Sl8nIBjIQrRQnuxmM5MY7td_secret_TiZx3ISyMFXuJfMv4rVKfhHXmT8O1nV&source_type=card#9-non-functional-requirements)++  
10. ++[Implementation Roadmap](https://claude.ai/chat/c7c29ce8-e8f6-400e-8429-1ad7d1c89a63?setup_intent=seti_1Sl8nIBjIQrRQnuxmM5MY7td&setup_intent_client_secret=seti_1Sl8nIBjIQrRQnuxmM5MY7td_secret_TiZx3ISyMFXuJfMv4rVKfhHXmT8O1nV&source_type=card#10-implementation-roadmap)++  
11. ++[Glossary](https://claude.ai/chat/c7c29ce8-e8f6-400e-8429-1ad7d1c89a63?setup_intent=seti_1Sl8nIBjIQrRQnuxmM5MY7td&setup_intent_client_secret=seti_1Sl8nIBjIQrRQnuxmM5MY7td_secret_TiZx3ISyMFXuJfMv4rVKfhHXmT8O1nV&source_type=card#11-glossary)++  
12. ++[Appendices](https://claude.ai/chat/c7c29ce8-e8f6-400e-8429-1ad7d1c89a63?setup_intent=seti_1Sl8nIBjIQrRQnuxmM5MY7td&setup_intent_client_secret=seti_1Sl8nIBjIQrRQnuxmM5MY7td_secret_TiZx3ISyMFXuJfMv4rVKfhHXmT8O1nV&source_type=card#12-appendices)++  
13. ++[References](https://claude.ai/chat/c7c29ce8-e8f6-400e-8429-1ad7d1c89a63?setup_intent=seti_1Sl8nIBjIQrRQnuxmM5MY7td&setup_intent_client_secret=seti_1Sl8nIBjIQrRQnuxmM5MY7td_secret_TiZx3ISyMFXuJfMv4rVKfhHXmT8O1nV&source_type=card#13-references)++  
  
## 1. System Overview  
## 1.1 Objective  
Implement a demand prioritization system for CTT (Portuguese Post) based on three proportional allocation methods: **Sainte-Laguë** (default), **D'Hondt**, and **WSJF** (Weighted Shortest Job First), operating across three hierarchical prioritization levels.  
## 1.2 Lean Portfolio Management Principles  
* **Flow-based prioritization**: Continuous prioritization based on economic value  
* **Transparency**: Clear visibility of prioritization criteria at all levels  
* **Decentralization with alignment**: Area autonomy with strategic alignment  
* **Value-driven**: Focus on business value delivered  
## 1.3 Key Features
* Multi-level prioritization (Requesting Area → Revenue Stream → Global)
* Three distinct allocation algorithms with different characteristics
* **Queue-based sequential prioritization** (NOW → NEXT → PRODUCTION)
* **Integration with BusinessMap lifecycle phases**
* CSV-based input/output for easy integration
* Automated weight normalization
* Comprehensive validation engine
* Audit trail and logging  
  
## 2. Target Operating Model (TOM) Structure  
## 2.1 Organizational Hierarchy  
```
CTT (Global)
├── Revenue Stream Group: eCommerce
│   └── Revenue Stream: eCommerce
│       ├── Budget Group: Commercial
│       ├── Budget Group: Operations
│       ├── Budget Group: Corporate
│       ├── Budget Group: CISO
│       ├── Budget Group: Data&AI
│       └── Budget Group: Technology
│
├── Revenue Stream Group: Mail & Services
│   ├── Revenue Stream: Mail
│   ├── Revenue Stream: Fulfilment
│   ├── Revenue Stream: Business Solutions
│   ├── Revenue Stream: Payments
│   └── Revenue Stream: Retail & Financial Services
│       └── (each RS has the same 6 Budget Groups)
│
└── Revenue Stream Group: Banco CTT
    └── Revenue Stream: Banco CTT
        └── (same 6 Budget Groups)

```
## 2.2 Revenue Streams  
1. **eCommerce**: Digital commerce platform and services  
2. **Mail**: Traditional and hybrid mail services  
3. **Fulfilment**: Logistics and warehouse services  
4. **Business Solutions**: B2B solutions and enterprise services  
5. **Payments**: Payment processing and financial transactions  
6. **Retail & Financial Services**: Retail network and financial products  
7. **Banco CTT**: Banking services  
## 2.3 Budget Groups  
All Revenue Streams share the same 6 Budget Groups:  
1. **Commercial**: Sales, marketing, product management  
2. **Operations**: Operational execution and delivery  
3. **Corporate**: Corporate functions (HR, Finance, Legal)  
4. **CISO**: Information security  
5. **Data&AI**: Data analytics and artificial intelligence  
6. **Technology**: IT infrastructure and development  
## 2.4 Delivery Model - Phases and Quality Gates  

| Macro Phase | Micro Phases |
| ----------- | ------------------------------------------------------------------------------------------ |
| Need | Backlog → In Definition → Pitch → Ready for Solution |
| Solution | In Definition → High Level Design → Ready for Approval → In Approval → Ready for Execution |
| Development | In Development → Ready for Acceptance → In Acceptance → Selected for Production |
| Production | In Rollout → In Production |

**Note**: IDEAs are created in **Backlog** phase and progress through quality gates.

## 2.5 Queue-Based Prioritization (v3.1)

The system implements **sequential queue-based prioritization** that separates IDEAs by their lifecycle stage, ensuring development work is prioritized over planning work.

### 2.5.1 Queue Definitions

**Queue Priority Order** (highest to lowest priority):

1. **NOW Queue** (Development Phase)
   - **Priority**: Highest (Ranks 1 to N)
   - **Purpose**: Active development work that must be completed
   - **Micro Phases**:
     - In Development
     - Ready for Acceptance
     - In Acceptance
     - Selected for Production
   - **Rationale**: Work-in-progress should be finished before starting new initiatives (Lean WIP limits)

2. **NEXT Queue** (Planning Phases - Need + Solution)
   - **Priority**: Lower (Ranks N+1 to M)
   - **Purpose**: Future work being defined and designed
   - **Micro Phases**:
     - Backlog
     - In Definition (Need)
     - Pitch
     - Ready for Solution
     - High Level Design
     - Ready for Approval
     - In Approval
     - Ready for Execution
   - **Rationale**: Planning work is important but secondary to completing active development

3. **PRODUCTION Queue**
   - **Priority**: No ranking (null rank)
   - **Purpose**: Tracking deployed solutions
   - **Micro Phases**:
     - In Rollout
     - In Production
   - **Rationale**: Already delivered, no prioritization needed

### 2.5.2 Sequential Ranking Logic

The system applies sequential ranking across queues:

```
Example with 8 NOW items and 10 NEXT items:

NOW Queue:
  Rank 1: IDEA002 - Checkout Optimization (In Development)
  Rank 2: IDEA003 - Mail Sorting Automation (In Acceptance)
  ...
  Rank 8: IDEA005 - Mobile Payment System (In Development)

NEXT Queue:
  Rank 9: IDEA006 - Customer Portal Enhancement (Backlog)
  Rank 10: IDEA009 - Mail API Integration (High Level Design)
  ...
  Rank 18: IDEA019 - Retail Customer Experience (Pitch)

PRODUCTION Queue:
  (No Rank): IDEA001 - New eCommerce Portal (In Production)
  (No Rank): IDEA012 - Banco CTT Mobile App (In Rollout)
```

### 2.5.3 Benefits

* **Finish Before Starting**: Encourages completion of active work before new initiatives
* **Clear Priorities**: Teams know development work takes precedence
* **Lean Compliance**: Limits Work-In-Progress (WIP) by prioritizing completion
* **Visibility**: Clear separation between active development and future planning
* **Alignment with BusinessMap**: Direct integration with portfolio tool lifecycle

## 3. Data Model  
## 3.1 Entity: IDEA
An IDEA represents a development request created by a Requesting Area.
**Mandatory Attributes**

| Attribute      | Type   | Description                          |
| -------------- | ------ | ------------------------------------ |
| ID             | string | Unique identifier for the IDEA       |
| Name           | string | Descriptive name of the IDEA         |
| RequestingArea | string | Requesting direction/department (RA) |
| RevenueStream  | string | Target Revenue Stream                |
| BudgetGroup    | string | Associated Budget Group              |

**Optional Attributes with Defaults**

| Attribute  | Type    | Default  | Range           | Description                                |
| ---------- | ------- | -------- | --------------- | ------------------------------------------ |
| Value      | float   | 1        | 1-10            | Expected business value                    |
| Urgency    | float   | 1        | 1-10            | Time criticality                           |
| Risk       | float   | 1        | 1-10            | Risk reduction/compliance                  |
| Size       | integer | 100      | > 0             | Estimated size (story points or hours)     |
| MicroPhase | string  | Backlog  | See section 2.4 | Current micro phase from BusinessMap       |

**Auto-Generated Attributes (v3.1)**

| Attribute | Type   | Description                                                     |
| --------- | ------ | --------------------------------------------------------------- |
| Queue     | string | Auto-assigned queue (NOW/NEXT/PRODUCTION) based on MicroPhase  |
  
**Calculated Attributes**

| Attribute                   | Type    | Description                                                                 |
| --------------------------- | ------- | --------------------------------------------------------------------------- |
| PriorityRA                  | integer | Priority within Requesting Area (1 to N)                                   |
| WSJF_Score                  | float   | WSJF score = (Value + Urgency + Risk) / Size                               |
| Priority_SainteLague_RS     | integer | Sainte-Laguë rank within Revenue Stream                                    |
| Priority_DHondt_RS          | integer | D'Hondt rank within Revenue Stream                                         |
| Priority_WSJF_RS            | integer | WSJF rank within Revenue Stream                                            |
| Priority_SainteLague_Global | integer | Sainte-Laguë global rank (sequential: NOW 1-N, NEXT N+1-M, PRODUCTION null)|
| Priority_DHondt_Global      | integer | D'Hondt global rank (sequential: NOW 1-N, NEXT N+1-M, PRODUCTION null)     |
| Priority_WSJF_Global        | integer | WSJF global rank (sequential: NOW 1-N, NEXT N+1-M, PRODUCTION null)        |
  
****3.2 Weight Structures****  
**Requesting Area Weights (Level 2)**  
**File**: weights_ra.csv  
```
RevenueStream,BudgetGroup,RequestingArea,Weight
eCommerce,Commercial,DIR_eCommerce_Commercial,30
eCommerce,Technology,DIR_Technology,25
eCommerce,Data&AI,DIR_DataAI,20
Mail,Operations,DIR_Mail_Operations,35
...

```
**Columns**:  
* RevenueStream: Revenue Stream name  
* BudgetGroup: Budget Group name  
* RequestingArea: Requesting Area identifier  
* Weight: Relative weight (should sum to 100 per RS, or will be normalized)  
**Revenue Stream Weights (Level 3)**  
**File**: weights_rs.csv  
```
RevenueStream,Weight
eCommerce,25
Mail,20
Fulfilment,15
Business Solutions,12
Payments,10
Retail & Financial Services,10
Banco CTT,8

```
**Columns**:  
* RevenueStream: Revenue Stream name  
* Weight: Relative strategic weight (should sum to 100, or will be normalized)  
  
## 4. Prioritization Methods  
## 4.1 Sainte-Laguë Method (Odd Divisor) - DEFAULT  
**Concept**  
Proportional representation method that tends to favor smaller parties/groups, using odd divisors. Provides balanced allocation across entities.  
**Quotient Formula**  
```
Q = Votes / (2 × Seats_already_allocated + 1)

```
**Algorithm**  
```
1. Initialize seat counters for each area = 0
2. For each priority position (1 to total IDEAs):
   a. Calculate quotient for each Requesting Area: Q = Weight_RA / (2 × Seats_RA + 1)
   b. Assign position to RA with highest quotient
   c. Within that RA, select next highest priority IDEA not yet allocated
   d. Increment seat counter for the RA
3. Repeat until all IDEAs are allocated

```
**When to Use**  
* **Default method** for balanced allocation  
* When seeking fair distribution across all areas  
* When smaller areas should have proportional representation  
**Example Calculation**  
**Setup**:  
* Area A: Weight = 60  
* Area B: Weight = 40  
* 4 IDEAs to allocate  

| Position | Area A Quotient | Area B Quotient | Winner | Seats A | Seats B |
| -------- | --------------- | --------------- | ------ | ------- | ------- |
| 1        | 60/(2×0+1)=60   | 40/(2×0+1)=40   | A      | 1       | 0       |
| 2        | 60/(2×1+1)=20   | 40/(2×0+1)=40   | B      | 1       | 1       |
| 3        | 60/(2×1+1)=20   | 40/(2×1+1)=13.3 | A      | 2       | 1       |
| 4        | 60/(2×2+1)=12   | 40/(2×1+1)=13.3 | B      | 2       | 2       |
  
**Result**: 2-2 allocation (balanced)  
## 4.2 D'Hondt Method (Hondt Divisor)  
**Concept**  
Proportional representation method that tends to favor larger parties/groups, using natural divisors. Reinforces strategic priorities.  
**Quotient Formula**  
```
Q = Votes / (Seats_already_allocated + 1)

```
**Algorithm**  
```
1. Initialize seat counters for each area = 0
2. For each priority position:
   a. Calculate quotient for each Requesting Area: Q = Weight_RA / (Seats_RA + 1)
   b. Assign position to RA with highest quotient
   c. Select next IDEA from that RA
   d. Increment seat counter for the RA
3. Repeat until all IDEAs are allocated

```
**Difference from Sainte-Laguë**  
Smaller divisor benefits areas that have already received allocations, creating a "winner takes more" effect.  
**When to Use**  
* When reinforcing strategic areas (those with higher weights)  
* When majority focus is desired  
* When consolidating resources on key initiatives  
**Example Calculation**  
**Same setup as above**:  

| Position | Area A Quotient | Area B Quotient | Winner | Seats A | Seats B |
| -------- | --------------- | --------------- | ------ | ------- | ------- |
| 1        | 60/(0+1)=60     | 40/(0+1)=40     | A      | 1       | 0       |
| 2        | 60/(1+1)=30     | 40/(0+1)=40     | B      | 1       | 1       |
| 3        | 60/(1+1)=30     | 40/(1+1)=20     | A      | 2       | 1       |
| 4        | 60/(2+1)=20     | 40/(1+1)=20     | A*     | 3       | 1       |
  
**Result**: 3-1 allocation (favors larger weight) *In case of tie, can use tiebreaker rules  
## 4.3 WSJF Method (Weighted Shortest Job First)  
**Concept**  
SAFe (Scaled Agile Framework) method that prioritizes work based on cost of delay divided by job size. Focuses on economic value independent of organizational structure.  
**Formula**  
```
WSJF = (Value + Urgency + Risk) / Size

Where:
- Value: Business value (1-10)
- Urgency: Time criticality (1-10)
- Risk: Risk reduction (1-10)
- Size: Estimated size (story points)

```
**Algorithm**  
**Level 2 (by RS)**:  
```
1. Calculate WSJF_Score for each IDEA
2. Apply RA weight as multiplier: Adjusted_WSJF = WSJF_Score × Weight_RA
3. Sort by Adjusted_WSJF (descending)
4. Assign ranks 1 to N

```
**Level 3 (Global)**:  
```
1. Use Level 2 results
2. Apply RS weight: Final_WSJF = Adjusted_WSJF × Weight_RS
3. Sort globally by Final_WSJF (descending)
4. Assign global ranks

```
**When to Use**  
* As complementary analysis to allocation methods  
* When pure economic value is the primary concern  
* For comparison with organizational priority methods  
* In highly dynamic environments requiring frequent reprioritization  
**Advantages**  
* Explicit consideration of multi-dimensional value  
* Accounts for job size (favors smaller, high-value work)  
* Mathematically simple and transparent  
**Limitations**  
* Ignores organizational constraints and politics  
* May concentrate work in specific areas  
* Requires accurate size estimation  
  
## 5. Prioritization Levels  
## 5.1 Level 1: Prioritization by Requesting Area  
**Responsibility**  
Each direction (Requesting Area) individually.  
**Process**  
1. Each RA analyzes its IDEAs considering:  
    * Strategic alignment  
    * Business value  
    * Technical dependencies  
    * Execution capacity  
2. Assigns sequential priority: 1, 2, 3, ..., N  
3. Defines values for Value, Urgency, Risk, Size (optional)  
**Output**
**File**: ideias.csv
```
ID;Name;RequestingArea;RevenueStream;BudgetGroup;MicroPhase;PriorityRA;Value;Urgency;Risk;Size
IDEA001;New eCommerce Portal;DIR_eCommerce_Commercial;eCommerce;Commercial;In Production;1;9;8;5;250
IDEA002;Checkout Optimization;DIR_eCommerce_Commercial;eCommerce;Commercial;In Development;2;7;9;3;100
IDEA003;Mail Sorting Automation;DIR_Mail_Operations;Mail;Operations;In Acceptance;1;8;10;7;300
IDEA004;ML Recommendations;DIR_DataAI;eCommerce;Data&AI;Ready for Execution;1;8;7;6;140
IDEA005;Mobile Payment System;DIR_Payments_Tech;Payments;Technology;In Development;1;7;9;6;180
...

```
**Validations**
* All mandatory fields filled
* PriorityRA sequential within each RA (no gaps)
* Value, Urgency, Risk between 1-10
* Size > 0
* RevenueStream valid (one of 7 defined)
* BudgetGroup valid (one of 6 defined)
* **MicroPhase valid** (v3.1) - one of 18 defined phases (see section 2.4)  
**Notes**  
* This level is performed **outside the system** to be built  
* The system receives ideias.csv as input  
## 5.2 Level 2: Prioritization by Revenue Stream  
**Inputs**  
* ideias.csv (from Level 1)  
* weights_ra.csv (Requesting Area weights)  
**Process**  
1. Load IDEAs and weights  
2. Group IDEAs by Revenue Stream  
3. For each Revenue Stream, apply all 3 methods:  
    * **Sainte-Laguë**: Use RA weights as "votes"  
    * **D'Hondt**: Use RA weights as "votes"  
    * **WSJF**: Sort by WSJF adjusted by RA weight  
4. Generate 3 rankings per RS  
**Output**  
**File**: prioritization_rs.csv  
```
RevenueStream,Method,Rank,ID,Name,RequestingArea,BudgetGroup,WSJF_Score,Value,Urgency,Risk,Size
eCommerce,SainteLague,1,IDEA001,New eCommerce Portal,DIR_eCommerce_Commercial,Commercial,0.088,9,8,5,250
eCommerce,SainteLague,2,IDEA004,ML Recommendations,DIR_DataAI,Data&AI,0.150,8,7,6,140
eCommerce,SainteLague,3,IDEA002,Checkout Optimization,DIR_eCommerce_Commercial,Commercial,0.190,7,9,3,100
eCommerce,DHondt,1,IDEA001,New eCommerce Portal,DIR_eCommerce_Commercial,Commercial,0.088,9,8,5,250
eCommerce,DHondt,2,IDEA002,Checkout Optimization,DIR_eCommerce_Commercial,Commercial,0.190,7,9,3,100
eCommerce,DHondt,3,IDEA004,ML Recommendations,DIR_DataAI,Data&AI,0.150,8,7,6,140
eCommerce,WSJF,1,IDEA002,Checkout Optimization,DIR_eCommerce_Commercial,Commercial,0.190,7,9,3,100
eCommerce,WSJF,2,IDEA004,ML Recommendations,DIR_DataAI,Data&AI,0.150,8,7,6,140
eCommerce,WSJF,3,IDEA001,New eCommerce Portal,DIR_eCommerce_Commercial,Commercial,0.088,9,8,5,250
Mail,SainteLague,1,IDEA003,Mail Sorting Automation,DIR_Mail_Operations,Operations,0.083,8,10,7,300
...

```
**Validations**  
* All IDEAs from the RS represented  
* Sequential rankings without gaps  
* Weights of RAs sum to 100 per RS (or normalize automatically)  
## 5.3 Level 3: Global CTT Prioritization (with Queue-Based Ranking v3.1)
**Inputs**
* prioritization_rs.csv (from Level 2)
* weights_rs.csv (Revenue Stream weights)
**Process**
1. Load RS prioritization and RS weights
2. **Determine Queue** for each IDEA based on MicroPhase (v3.1):
   * NOW queue: Development phases (In Development, Ready for Acceptance, In Acceptance, Selected for Production)
   * NEXT queue: Planning phases (Need + Solution phases)
   * PRODUCTION queue: Production phases (In Rollout, In Production)
3. For each method (Sainte-Laguë, D'Hondt, WSJF):
   * **Process NOW queue first** → Ranks 1 to N (highest priority)
   * **Process NEXT queue second** → Ranks N+1 to M (lower priority)
   * **Process PRODUCTION queue** → No ranking (null)
4. Consolidate results with sequential global ranking

**Output**
**File**: demand.csv
```
Queue;Method;GlobalRank;ID;Name;RequestingArea;RevenueStream;BudgetGroup;MicroPhase;PriorityRA;WSJF_Score;Value;Urgency;Risk;Size
NOW;SainteLague;1;IDEA002;Checkout Optimization;DIR_eCommerce_Commercial;eCommerce;Commercial;In Development;2;0,190;7;9;3;100
NOW;SainteLague;2;IDEA003;Mail Sorting Automation;DIR_Mail_Operations;Mail;Operations;In Acceptance;1;0,083;8;10;7;300
NOW;SainteLague;3;IDEA005;Mobile Payment System;DIR_Payments_Tech;Payments;Technology;In Development;1;0,122;7;9;6;180
...
NOW;SainteLague;8;IDEA007;Fulfilment Tracking;DIR_Fulfilment_Ops;Fulfilment;Operations;Ready for Acceptance;1;0,115;8;8;7;200
NEXT;SainteLague;9;IDEA004;ML Recommendations;DIR_DataAI;eCommerce;Data&AI;Ready for Execution;1;0,150;8;7;6;140
NEXT;SainteLague;10;IDEA006;Customer Portal;DIR_eCommerce_Commercial;eCommerce;Commercial;Backlog;3;0,142;6;7;4;120
...
NEXT;SainteLague;18;IDEA019;Retail Customer Experience;DIR_Retail_Commercial;Retail & Financial Services;Commercial;Pitch;1;0,111;7;8;5;180
PRODUCTION;sainte-lague;;IDEA001;New eCommerce Portal;DIR_eCommerce_Commercial;eCommerce;Commercial;In Production;1;;9;8;5;250
PRODUCTION;sainte-lague;;IDEA012;Banco CTT Mobile App;DIR_Banco_Tech;Banco CTT;Technology;In Rollout;1;;8;9;7;280
...

```
**Validations**
* NOW queue: Global rankings sequential (1 to N) per method
* NEXT queue: Global rankings sequential (N+1 to M) per method
* PRODUCTION queue: No ranking (GlobalRank is null)
* All IDEAs represented in each method
* Weights of RS sum to 100 (or normalize automatically)

**Sequential Ranking Logic (v3.1)**
* Development work (NOW) always ranks higher than planning work (NEXT)
* Within each queue, standard prioritization algorithms apply
* PRODUCTION items are tracked but not prioritized  
  
## 6. Functional Specification  
## 6.1 System Architecture  
```
┌─────────────────────────────────────────────────────────┐
│                   TOM Demand Manager                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Loader     │  │ Prioritizer  │  │   Exporter   │ │
│  │   Module     │  │   Module     │  │    Module    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│         │                  │                  │         │
│         ├──────────────────┼──────────────────┤         │
│         │                  │                  │         │
│  ┌──────▼──────────────────▼──────────────────▼──────┐ │
│  │            Data Validation Engine                │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─────────────────────────────────────────────────────┐ │
│  │         Prioritization Algorithms               │ │
│  │  • Sainte-Laguë  • D'Hondt  • WSJF             │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘

```
## 6.2 Functional Modules  
**6.2.1 Loader Module**  
**Responsibility**: Load and validate input data  
**Functions**:  
```
def load_ideas(filepath: str) -> pd.DataFrame:
    """
    Load and validate ideas from CSV file.
    
    Args:
        filepath: Path to ideias.csv
        
    Returns:
        DataFrame with validated IDEAs
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValidationError: If data validation fails
    """

def load_ra_weights(filepath: str) -> pd.DataFrame:
    """
    Load Requesting Area weights from CSV file.
    
    Args:
        filepath: Path to weights_ra.csv
        
    Returns:
        DataFrame with validated RA weights
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValidationError: If data validation fails
    """

def load_rs_weights(filepath: str) -> pd.DataFrame:
    """
    Load Revenue Stream weights from CSV file.
    
    Args:
        filepath: Path to weights_rs.csv
        
    Returns:
        DataFrame with validated RS weights
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValidationError: If data validation fails
    """

```
**Validations**:  
* File existence  
* Column structure validation  
* Data type checking  
* Range validation (Value, Urgency, Risk: 1-10; Size > 0)  
* Referential integrity (RAs exist in weights, RS valid)  
**Output**: Validated DataFrames or exceptions with clear error messages  
**6.2.2 Validator Module**  
**Responsibility**: Centralized data validation  
**Validation Rules**:  
**1. IDEAs (ideias.csv)**:  
* ID: Unique, non-empty string  
* Name: Non-empty string  
* RequestingArea: Must exist in weights_ra.csv  
* RevenueStream: Valid (one of 7 defined RS)  
* BudgetGroup: Valid (one of 6 defined BG)  
* PriorityRA: Positive integer, sequential per RA  
* Value, Urgency, Risk: Between 1-10 (inclusive)  
* Size: Greater than 0  
**2. RA Weights (weights_ra.csv)**:  
* Combination (RevenueStream, BudgetGroup, RequestingArea) must be unique  
* Weight: Greater than 0  
* Sum of weights per RS should equal 100 (or auto-normalize)  
**3. RS Weights (weights_rs.csv)**:  
* RevenueStream: Unique and valid  
* Weight: Greater than 0  
* Sum of weights should equal 100 (or auto-normalize)  
**Error Handling**:  
* **Critical errors**: Stop execution with clear message  
* **Warnings**: Log but allow continuation (e.g., weight normalization)  
**Functions**:  
```
def validate_ideas(df: pd.DataFrame, ra_weights: pd.DataFrame) -> ValidationResult:
    """Validate IDEAS dataframe"""

def validate_ra_weights(df: pd.DataFrame) -> ValidationResult:
    """Validate RA weights dataframe"""

def validate_rs_weights(df: pd.DataFrame) -> ValidationResult:
    """Validate RS weights dataframe"""

def normalize_weights(df: pd.DataFrame, group_by: List[str]) -> pd.DataFrame:
    """Normalize weights to sum to 100 within groups"""

```
**6.2.3 Prioritizer Module**  
**Responsibility**: Execute prioritization algorithms  
**Core Functions**:  
```
def prioritize_level2(
    ideas: pd.DataFrame,
    ra_weights: pd.DataFrame,
    method: str  # 'sainte-lague' | 'dhondt' | 'wsjf'
) -> pd.DataFrame:
    """
    Prioritize IDEAs by Revenue Stream using specified method.
    
    Args:
        ideas: DataFrame with IDEAs
        ra_weights: DataFrame with RA weights
        method: Prioritization method to use
        
    Returns:
        DataFrame with prioritized IDEAs per RS and method
    """

def prioritize_level3(
    rs_prioritized: pd.DataFrame,
    rs_weights: pd.DataFrame,
    method: str
) -> pd.DataFrame:
    """
    Prioritize IDEAs globally using specified method.
    
    Args:
        rs_prioritized: DataFrame from Level 2
        rs_weights: DataFrame with RS weights
        method: Prioritization method to use
        
    Returns:
        DataFrame with global prioritization
    """

def calculate_wsjf(idea: Dict) -> float:
    """
    Calculate WSJF score: (Value + Urgency + Risk) / Size
    
    Args:
        idea: Dictionary with IDEA attributes
        
    Returns:
        WSJF score (float)
    """

```
**Algorithm Implementations**:  
**Sainte-Laguë Algorithm**  
```
def sainte_lague_allocate(
    entities: List[str],
    weights: Dict[str, float],
    items: List[Dict],
    level: str  # 'RS' | 'Global'
) -> List[Dict]:
    """
    Allocate items using Sainte-Laguë method.
    
    Algorithm:
    1. Initialize seat counters to 0 for all entities
    2. For each position from 1 to N:
       a. Calculate quotient for each entity: Q = Weight / (2 * Seats + 1)
       b. Select entity with highest quotient
       c. Allocate next item from that entity
       d. Increment seat counter
    3. Return allocated items with ranks
    
    Args:
        entities: List of entity identifiers (RAs or RSs)
        weights: Dictionary mapping entities to weights
        items: List of items to allocate
        level: Allocation level ('RS' or 'Global')
        
    Returns:
        List of items with assigned ranks
    """
    # Initialize
    seats = {entity: 0 for entity in entities}
    allocation = []
    
    # Group items by entity
    items_by_entity = group_items_by_entity(items, level)
    
    # Allocate each item
    for position in range(1, len(items) + 1):
        # Calculate quotients
        quotients = {}
        for entity in entities:
            if has_remaining_items(entity, items_by_entity, allocation):
                quotients[entity] = weights[entity] / (2 * seats[entity] + 1)
            else:
                quotients[entity] = 0
        
        # Select entity with highest quotient
        selected_entity = max(quotients, key=quotients.get)
        
        # Select next item from that entity
        next_item = get_next_item(selected_entity, items_by_entity, allocation)
        next_item['Rank'] = position
        next_item['Method'] = 'SainteLague'
        allocation.append(next_item)
        
        # Increment seats
        seats[selected_entity] += 1
    
    return allocation

```
**D'Hondt Algorithm**  
```
def dhondt_allocate(
    entities: List[str],
    weights: Dict[str, float],
    items: List[Dict],
    level: str
) -> List[Dict]:
    """
    Allocate items using D'Hondt method.
    
    Algorithm:
    1. Initialize seat counters to 0 for all entities
    2. For each position from 1 to N:
       a. Calculate quotient for each entity: Q = Weight / (Seats + 1)
       b. Select entity with highest quotient
       c. Allocate next item from that entity
       d. Increment seat counter
    3. Return allocated items with ranks
    
    Args:
        entities: List of entity identifiers
        weights: Dictionary mapping entities to weights
        items: List of items to allocate
        level: Allocation level
        
    Returns:
        List of items with assigned ranks
    """
    seats = {entity: 0 for entity in entities}
    allocation = []
    items_by_entity = group_items_by_entity(items, level)
    
    for position in range(1, len(items) + 1):
        quotients = {}
        for entity in entities:
            if has_remaining_items(entity, items_by_entity, allocation):
                quotients[entity] = weights[entity] / (seats[entity] + 1)
            else:
                quotients[entity] = 0
        
        selected_entity = max(quotients, key=quotients.get)
        next_item = get_next_item(selected_entity, items_by_entity, allocation)
        next_item['Rank'] = position
        next_item['Method'] = 'DHondt'
        allocation.append(next_item)
        seats[selected_entity] += 1
    
    return allocation

```
**WSJF Algorithm**  
```
def wsjf_prioritize(
    ideas: pd.DataFrame,
    weights: Dict[str, float],
    level: str  # 'RS' | 'Global'
) -> pd.DataFrame:
    """
    Prioritize using WSJF method.
    
    Algorithm:
    Level 2 (RS):
    1. Calculate WSJF_Score for each IDEA
    2. Apply RA weight: Adjusted_WSJF = WSJF_Score × Weight_RA
    3. Sort by Adjusted_WSJF (descending)
    4. Assign ranks
    
    Level 3 (Global):
    1. Use Level 2 Adjusted_WSJF
    2. Apply RS weight: Final_WSJF = Adjusted_WSJF × Weight_RS
    3. Sort by Final_WSJF (descending)
    4. Assign global ranks
    
    Args:
        ideas: DataFrame with IDEAs
        weights: Dictionary with entity weights
        level: Calculation level

```
  
Returns: DataFrame with WSJF-prioritized IDEAs """ # Calculate base WSJF score ideas['WSJF_Score'] = ( ideas['Value'] + ideas['Urgency'] + ideas['Risk'] ) / ideas['Size']  
```
# Apply weights based on level
if level == 'RS':
    ideas['Adjusted_WSJF'] = ideas.apply(
        lambda row: row['WSJF_Score'] * weights[row['RequestingArea']], 
        axis=1
    )
    sort_key = 'Adjusted_WSJF'
else:  # Global
    ideas['Final_WSJF'] = ideas.apply(
        lambda row: row['Adjusted_WSJF'] * weights[row['RevenueStream']], 
        axis=1
    )
    sort_key = 'Final_WSJF'

# Sort and assign ranks
ideas_sorted = ideas.sort_values(sort_key, ascending=False).reset_index(drop=True)
ideas_sorted['Rank'] = range(1, len(ideas_sorted) + 1)
ideas_sorted['Method'] = 'WSJF'

return ideas_sorted

**Helper Functions**:

```python
def group_items_by_entity(items: List[Dict], level: str) -> Dict:
    """Group items by entity (RA or RS) sorted by priority"""

def has_remaining_items(entity: str, items_by_entity: Dict, allocation: List) -> bool:
    """Check if entity has items not yet allocated"""

def get_next_item(entity: str, items_by_entity: Dict, allocation: List) -> Dict:
    """Get next unallocated item from entity"""

```
**6.2.4 Exporter Module**  
**Responsibility**: Export results to CSV files  
**Functions**:  
```
def export_rs_prioritization(
    data: pd.DataFrame, 
    filepath: str,
    metadata: Dict = None
) -> None:
    """
    Export Level 2 prioritization to CSV.
    
    Args:
        data: DataFrame with RS-level prioritization
        filepath: Output file path
        metadata: Optional metadata to include
    """

def export_demand(
    data: pd.DataFrame, 
    filepath: str,
    metadata: Dict = None
) -> None:
    """
    Export Level 3 global prioritization to CSV.
    
    Args:
        data: DataFrame with global prioritization
        filepath: Output file path
        metadata: Optional metadata to include
    """

def export_comparison_report(
    data: Dict[str, pd.DataFrame], 
    filepath: str
) -> None:
    """
    Export comparison report of all 3 methods.
    
    Args:
        data: Dictionary with results from all methods
        filepath: Output file path
    """

def export_metadata(
    execution_params: Dict,
    filepath: str
) -> None:
    """
    Export execution metadata (parameters, timestamps, etc.).
    
    Args:
        execution_params: Dictionary with execution parameters
        filepath: Output file path (JSON)
    """

```
**Output Formats**: As specified in sections 5.2 and 5.3  
**Metadata Structure** (metadata.json):  
```
{
  "execution_timestamp": "2026-01-02T10:30:00Z",
  "system_version": "3.0",
  "input_files": {
    "ideas": "ideias_q1_2026.csv",
    "ra_weights": "weights_ra_q1.csv",
    "rs_weights": "weights_rs_q1.csv"
  },
  "output_files": {
    "level2": "prioritization_rs.csv",
    "level3": "demand.csv"
  },
  "statistics": {
    "total_ideas": 247,
    "total_requesting_areas": 18,
    "total_revenue_streams": 7
  },
  "methods_executed": ["SainteLague", "DHondt", "WSJF"],
  "weights_normalized": true
}

```
## 6.3 Command Line Interface (CLI)  
**Complete Prioritization (Levels 2 and 3)**  
```
# Execute complete prioritization with default method (Sainte-Laguë)
python tom_demand.py prioritize \
  --ideas ideias.csv \
  --ra-weights weights_ra.csv \
  --rs-weights weights_rs.csv \
  --output-dir ./output

# Execute with specific method
python tom_demand.py prioritize \
  --ideas ideias.csv \
  --ra-weights weights_ra.csv \
  --rs-weights weights_rs.csv \
  --method dhondt \
  --output-dir ./output

# Execute all methods
python tom_demand.py prioritize \
  --ideas ideias.csv \
  --ra-weights weights_ra.csv \
  --rs-weights weights_rs.csv \
  --all-methods \
  --output-dir ./output

```
**Level 2 Only**  
```
# Execute Level 2 only
python tom_demand.py prioritize-rs \
  --ideas ideias.csv \
  --ra-weights weights_ra.csv \
  --method sainte-lague \
  --output prioritization_rs.csv

```
**Level 3 Only**  
```
# Execute Level 3 only
python tom_demand.py prioritize-global \
  --rs-prioritized prioritization_rs.csv \
  --rs-weights weights_rs.csv \
  --method dhondt \
  --output demand.csv

```
**Method Comparison**  
```
# Compare all 3 methods
python tom_demand.py compare \
  --ideas ideias.csv \
  --ra-weights weights_ra.csv \
  --rs-weights weights_rs.csv \
  --output comparison_report.csv \
  --top-n 50

```
**Validation Only**  
```
# Validate input files without executing prioritization
python tom_demand.py validate \
  --ideas ideias.csv \
  --ra-weights weights_ra.csv \
  --rs-weights weights_rs.csv

```
**CLI Parameters**  

| Parameter | Type | Default | Description |
| ------------------- | ------- | ------------ | -------------------------------------------------- |
| --ideas | string | Required | Path to ideias.csv |
| --ra-weights | string | Required | Path to weights_ra.csv |
| --rs-weights | string | Required | Path to weights_rs.csv |
| --method | string | sainte-lague | Prioritization method (sainte-lague, dhondt, wsjf) |
| --all-methods | flag | False | Execute all 3 methods |
| --output-dir | string | ./output | Output directory |
| --output | string | Auto | Specific output file path |
| --normalize-weights | flag | True | Auto-normalize weights to sum 100 |
| --top-n | integer | None | Show only top N results |
| --verbose | string | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| --config | string | config.yaml | Configuration file path |
  
**CLI Output Examples**  
**Validation Success**:  
```
✓ Validating input files...
  ✓ ideias.csv: 247 IDEAs loaded successfully
  ✓ weights_ra.csv: 18 Requesting Areas loaded
  ✓ weights_rs.csv: 7 Revenue Streams loaded
  ⚠ Normalizing RA weights for eCommerce (sum=98.5 → 100)
✓ All validations passed

Summary:
  - Total IDEAs: 247
  - Requesting Areas: 18
  - Revenue Streams: 7
  - Average IDEA Size: 156 story points

```
**Prioritization Execution**:  
```
✓ Starting prioritization process...
  ✓ Level 2: Prioritizing by Revenue Stream
    - eCommerce: 78 IDEAs prioritized
    - Mail: 54 IDEAs prioritized
    - Fulfilment: 32 IDEAs prioritized
    - Business Solutions: 28 IDEAs prioritized
    - Payments: 24 IDEAs prioritized
    - Retail & Financial Services: 19 IDEAs prioritized
    - Banco CTT: 12 IDEAs prioritized
  ✓ Level 3: Global prioritization
    - Method: Sainte-Laguë
    - 247 IDEAs ranked globally
✓ Prioritization complete

Output files:
  - ./output/prioritization_rs.csv
  - ./output/demand.csv
  - ./output/metadata.json

Execution time: 2.3 seconds

```
## 6.4 Configuration File  
**File**: config.yaml  
```
# TOM Demand Management System Configuration

# Organizational Structure
revenue_streams:
  - eCommerce
  - Mail
  - Fulfilment
  - Business Solutions
  - Payments
  - Retail & Financial Services
  - Banco CTT

budget_groups:
  - Commercial
  - Operations
  - Corporate
  - CISO
  - Data&AI
  - Technology

# Default values for optional IDEA attributes
defaults:
  value: 1
  urgency: 1
  risk: 1
  size: 100

# Validation ranges
validation:
  value_range: [1, 10]
  urgency_range: [1, 10]
  risk_range: [1, 10]
  size_min: 1

# Prioritization settings
prioritization:
  default_method: sainte-lague  # sainte-lague | dhondt | wsjf
  auto_normalize_weights: true
  tie_breaker: priority_ra  # priority_ra | wsjf_score | alphabetical

# Output settings
output:
  include_metadata: true
  decimal_precision: 3
  date_format: "%Y-%m-%d %H:%M:%S"

# Logging
logging:
  level: INFO  # DEBUG | INFO | WARNING | ERROR
  file: tom_demand.log
  console_output: true
  log_rotation: true
  max_log_size_mb: 10

# Performance
performance:
  parallel_processing: false
  chunk_size: 1000

```
  
## 7. Use Cases and Examples  
## 7.1 Use Case 1: Quarterly Prioritization  
**Context**: Beginning of Q2 2026, need to prioritize complete backlog  
**Steps**:  
1. Each direction prioritizes their IDEAs → ideias_q2_2026.csv  
2. Portfolio Manager defines RA weights → weights_ra_q2.csv  
3. CFO defines strategic RS weights → weights_rs_q2.csv  
4. Execute system: python tom_demand.py prioritize \  --ideas ideias_q2_2026.csv \  --ra-weights weights_ra_q2.csv \  --rs-weights weights_rs_q2.csv \  --all-methods \  --output-dir ./output/q2_2026  
5.   
6. Analyze demand.csv and decide which method to adopt (default: Sainte-Laguë)  
7. Communicate prioritization to development teams  
**Expected Outcomes**:  
* Clear global priority list for Q2  
* Visibility of trade-offs between methods  
* Alignment between strategic weights and execution priority  
## 7.2 Use Case 2: Sensitivity Analysis  
**Context**: Evaluate impact of changes in RS weights  
**Steps**:  
1. Create 3 weight scenarios:  
    * weights_rs_balanced.csv (current: eCommerce 25%)  
    * weights_rs_ecommerce_focus.csv (eCommerce 35%)  
    * weights_rs_mail_focus.csv (Mail 30%)  
2. Execute for each scenario:for scenario in balanced ecommerce_focus mail_focus; do  
3.   python tom_demand.py prioritize \  
4.     --ideas ideias.csv \  
5.     --ra-weights weights_ra.csv \  
6.     --rs-weights weights_rs_$scenario.csv \  
7.     --output-dir ./output/scenario_$scenario  
8. done  
9.   
10. Compare top 20 IDEAs in each scenario  
11. Identify IDEAs sensitive to strategic changes  
**Analysis Output**:  

| IDEA    | Balanced Rank | eComm Focus Rank | Mail Focus Rank | Volatility |
| ------- | ------------- | ---------------- | --------------- | ---------- |
| IDEA001 | 1             | 1                | 3               | Low        |
| IDEA003 | 2             | 5                | 1               | High       |
| IDEA015 | 8             | 3                | 12              | High       |
  
**Insight**: IDEAs with high volatility require careful strategic consideration.  
## 7.3 Use Case 3: Method Comparison  
**Context**: Understand differences between Sainte-Laguë, D'Hondt, and WSJF  
**Simplified Example**:  
**Input** (4 IDEAs, 2 RAs, 1 RS):  
```
ID,Name,RequestingArea,RevenueStream,PriorityRA,Value,Urgency,Risk,Size
I1,Portal,RA1,eCommerce,1,9,8,5,250
I2,Checkout,RA1,eCommerce,2,7,9,3,100
I3,ML,RA2,eCommerce,1,8,7,6,140
I4,Analytics,RA2,eCommerce,2,6,5,4,80

```
**RA Weights**: RA1=60%, RA2=40%  
**WSJF Calculation**:  
* I1: (9+8+5)/250 = 0.088  
* I2: (7+9+3)/100 = 0.190  
* I3: (8+7+6)/140 = 0.150  
* I4: (6+5+4)/80 = 0.188  
**Results (Level 2 - Revenue Stream)**:  

| Rank | Sainte-Laguë | Quotients | D'Hondt | Quotients | WSJF | Scores |
| ---- | ------------ | --------- | -------- | --------- | -------- | ------------- |
| 1 | I1 (RA1) | 60/1=60 | I1 (RA1) | 60/1=60 | I2 (RA1) | 0.190×60=11.4 |
| 2 | I3 (RA2) | 40/1=40 | I2 (RA1) | 60/2=30 | I3 (RA2) | 0.150×40=6.0 |
| 3 | I2 (RA1) | 60/3=20 | I3 (RA2) | 40/1=40 | I4 (RA2) | 0.188×40=7.5 |
| 4 | I4 (RA2) | 40/3=13.3 | I4 (RA2) | 40/2=20 | I1 (RA1) | 0.088×60=5.3 |
  
**Analysis**:  
* **Sainte-Laguë**: Best distribution between RA1 and RA2 (2-2 split)  
* **D'Hondt**: Favors RA1 due to higher weight (3-1 split)  
* **WSJF**: Ignores organizational weights, focuses purely on economic ROI  
**When to Use Each Method**:  

| Method | Best For | Trade-offs |
| ------------ | ----------------------------------------------- | ------------------------------------- |
| Sainte-Laguë | Balanced allocation across all areas | May dilute strategic focus |
| D'Hondt | Reinforcing strategic areas with higher weights | Smaller areas get less representation |
| WSJF | Pure economic value optimization | Ignores organizational constraints |
  
**Recommendation**: Use **Sainte-Laguë as default**, with D'Hondt for strategic focus periods, and WSJF for economic validation.  
## 7.4 Use Case 4: New Strategic Initiative  
**Context**: New CEO wants to triple investment in Data&AI across all Revenue Streams  
**Process**:  
1. Update weights_ra.csv:  
    * Increase Data&AI weight from ~15% to ~35% per RS  
    * Rebalance other BG weights proportionally  
2. Execute prioritization:python tom_demand.py prioritize \  
3.   --ideas ideias.csv \  
4.   --ra-weights weights_ra_datai_focus.csv \  
5.   --rs-weights weights_rs.csv \  
6.   --method sainte-lague \  
7.   --output-dir ./output/datai_initiative  
8.   
9. Compare with previous prioritization:python tom_demand.py compare \  
10.   --ideas ideias.csv \  
11.   --ra-weights weights_ra_previous.csv \  
12.   --rs-weights weights_rs.csv \  
13.   --output comparison_before_after.csv  
14.   
15. Identify Data&AI IDEAs that moved into top 50  
**Expected Impact**:  
* Data&AI IDEAs rise ~100 positions on average  
* Some operational IDEAs deferred  
* Clear message to organization about strategic shift  
  
## 8. Integration with TOM Delivery Model  
## 8.1 Quality Gates and Prioritization  
**Relationship between Prioritization and Phases**:  
**Gate 1: Backlog → In Definition**  
**Trigger**: IDEA enters top N of global prioritization (N defined by capacity)  
**Criteria**:  
* Priority_SainteLague_Global ≤ capacity_threshold  
* All mandatory IDEA attributes filled  
* Assigned Product Owner  
**Actions**:  
* Activate IDEA in project management tool  
* Schedule definition workshop  
* Assign resources  
**Gate 2: Pitch → Ready for Solution**  
**Trigger**: IDEA passes pitch to stakeholders  
**Note**: Reprioritization can occur before this gate. IDEAs that drop in priority may be paused.  
**Criteria**:  
* Business case approved  
* Still within capacity threshold  
* Technical feasibility confirmed  
**Gate 3: Ready for Execution → In Development**  
**Trigger**: Final prioritization determines sprint/PI Planning order  
**Criteria**:  
* Solution approved and funded  
* Team capacity available  
* Dependencies resolved  
**Prioritization Reference**: Final demand.csv ranking  
## 8.2 Reprioritization Mechanism  
**Frequency**: Monthly (or per PI in SAFe context)  
**Events Triggering Reprioritization**:  
1. **Strategic changes**: Adjustment of RS weights  
2. **Critical new IDEAs**: Urgency > 8 or regulatory requirement  
3. **Completion of major initiatives**: Capacity freed up  
4. **External factors**: Market changes, competition, regulations  
**Reprioritization Process**:  
```
1. Update inputs (ideias.csv, weights)
2. Execute prioritization
3. Compare with previous ranking
4. Identify significant changes (>20 position delta)
5. Communicate to stakeholders
6. Update project management tools
7. Adjust team allocations if needed

```
**Change Threshold Policy**:  

| Position Change  | Action                        |
| ---------------- | ----------------------------- |
| ±1-10 positions  | No action, natural variance   |
| ±11-20 positions | Inform Product Owner          |
| ±21-50 positions | Review with Portfolio Manager |
| >±50 positions   | Executive review required     |
  
****8.3 Capacity vs. Demand****  
**Capacity Calculation by RS**:  
```
# Example for eCommerce RS
capacity_ecommerce = {
    'Technology': 500,      # story points per sprint
    'Data&AI': 200,
    'Commercial': 100,
    'Operations': 150,
    'CISO': 50,
    'Corporate': 30
}

# Total capacity eCommerce = 1030 SP/sprint
# If backlog = 5000 SP → 4.85 sprints of work

```
**Visualization in Output**:  
Enhanced demand.csv with capacity columns:  
```
Method,GlobalRank,ID,Name,RevenueStream,BudgetGroup,Size,CumulativeSize,CanStartSprint,EstimatedCompletionSprint
SainteLague,1,IDEA001,Portal,eCommerce,Technology,250,250,1,1
SainteLague,2,IDEA003,Sorting,Mail,Operations,300,550,1,2
SainteLague,3,IDEA015,Payments,Payments,Technology,180,730,1,2
SainteLague,4,IDEA008,Analytics,eCommerce,Data&AI,200,930,1,3
SainteLague,5,IDEA012,Automation,Mail,Operations,350,1280,2,4

```
**Capacity Planning Report**:  
```
Revenue Stream: eCommerce
- Total Demand: 3,450 SP
- Sprint Capacity: 1,030 SP
- Estimated Duration: 3.4 sprints
- Top 10 IDEAs: 1,800 SP (1.7 sprints)

Revenue Stream: Mail
- Total Demand: 2,100 SP
- Sprint Capacity: 650 SP
- Estimated Duration: 3.2 sprints
- Top 10 IDEAs: 1,200 SP (1.8 sprints)

```
## 8.4 Metrics and KPIs  
**Prioritization Health Metrics**:  
1. **Execution Alignment**: % of completed work that was in top 50 priority  
2. **Priority Stability**: Average position change between reprioritizations  
3. **Throughput**: Average time from Backlog to Production  
4. **Value Realization**: Actual value delivered vs. estimated  
5. **Capacity Utilization**: Actual work vs. planned capacity  
**Dashboard KPIs**:  
```
Current Quarter Status:
┌─────────────────────────────────────────────┐
│ Top 50 IDEAs                                │
│ ● In Development: 12 (24%)                  │
│ ● In Solution: 18 (36%)                     │
│ ● In Definition: 15 (30%)                   │
│ ● In Backlog: 5 (10%)                       │
└─────────────────────────────────────────────┘

Execution vs. Priority:
┌─────────────────────────────────────────────┐
│ ✓ Top 20 completed: 85%                     │
│ ✓ Top 50 completed: 72%                     │
│ ✗ Out-of-priority: 15% (investigate)        │
└─────────────────────────────────────────────┘

```
  
## 9. Non-Functional Requirements  
## 9.1 Performance  

| Metric                  | Requirement  | Target       |
| ----------------------- | ------------ | ------------ |
| Process 1000 IDEAs      | < 10 seconds | < 5 seconds  |
| Process 50 RAs          | < 15 seconds | < 10 seconds |
| Complete prioritization | < 20 seconds | < 15 seconds |
| Memory usage            | < 1GB        | < 500MB      |
| Concurrent executions   | Support 5    | Support 10   |
  
****9.2 Usability****  
* **CLI help**: Comprehensive --help for all commands  
* **Error messages**: Clear, actionable messages with suggested fixes  
* **Progress indicators**: Real-time progress bars for long operations  
* **Output preview**: Show top 10 results in console  
* **Validation feedback**: Immediate validation with clear pass/fail  
**Example Error Message**:  
```
❌ Error: Invalid IDEA detected

Details:
  - IDEA ID: IDEA042
  - Field: Value
  - Issue: Value 12 exceeds maximum of 10
  - Location: ideias.csv, row 43

Suggestion: Update Value to be between 1 and 10

To fix:
  1. Open ideias.csv
  2. Find row with ID=IDEA042
  3. Change Value from 12 to a value between 1-10
  4. Re-run validation

```
## 9.3 Maintainability  
* **Modular architecture**: Clear separation of concerns  
* **Code documentation**: Docstrings in English for all functions  
* **Unit tests**: >80% code coverage  
* **Integration tests**: Full end-to-end scenarios  
* **Type hints**: Python type annotations throughout  
* **Logging**: Structured logging for debugging  
**Code Quality Standards**:  
```
# Example with full documentation and type hints
def prioritize_level2(
    ideas: pd.DataFrame,
    ra_weights: pd.DataFrame,
    method: str = 'sainte-lague'
) -> pd.DataFrame:
    """
    Prioritize IDEAs by Revenue Stream using specified method.
    
    This function takes IDEAs and RA weights, groups by Revenue Stream,
    and applies the specified prioritization algorithm to generate
    rankings within each RS.
    
    Args:
        ideas: DataFrame containing validated IDEAs with columns:
               ['ID', 'Name', 'RequestingArea', 'RevenueStream', 
                'BudgetGroup', 'PriorityRA', 'Value', 'Urgency', 'Risk', 'Size']
        ra_weights: DataFrame with RA weights, columns:
                    ['RevenueStream', 'BudgetGroup', 'RequestingArea', 'Weight']
        method: Prioritization method, one of:
                - 'sainte-lague' (default): Balanced allocation
                - 'dhondt': Strategic area focus
                - 'wsjf': Economic value focus
    
    Returns:
        DataFrame with prioritized IDEAs including new columns:
        ['Method', 'Rank', 'WSJF_Score']
    
    Raises:
        ValueError: If method is not recognized
        DataError: If ideas or ra_weights have missing required columns
    
    Example:
        >>> ideas = pd.read_csv('ideias.csv')
        >>> weights = pd.read_csv('weights_ra.csv')
        >>> result = prioritize_level2(ideas, weights, method='sainte-lague')
        >>> print(result.head())
    """

```
## 9.4 Portability  
* **Python version**: 3.9+  
* **Operating systems**: Windows, macOS, Linux  
* **Dependencies**: Minimal external dependencies  
    * pandas >= 1.3.0  
    * numpy >= 1.21.0  
    * pyyaml >= 5.4.0  
* **Deployment**: Single executable via PyInstaller (optional)  
* **Configuration**: Environment-agnostic YAML config  
## 9.5 Auditability  
**Logging Requirements**:  
* All executions logged with timestamp  
* Input file checksums recorded  
* Execution parameters stored  
* Output file references tracked  
* User/system identification (if applicable)  
**Audit Log Format**:  
```
{
  "timestamp": "2026-01-02T10:30:45.123Z",
  "execution_id": "exec_20260102_103045",
  "user": "portfolio_manager",
  "command": "prioritize",
  "inputs": {
    "ideas": {
      "path": "ideias_q1_2026.csv",
      "checksum": "a3b2c1d4...",
      "row_count": 247
    },
    "ra_weights": {
      "path": "weights_ra_q1.csv",
      "checksum": "e5f6g7h8...",
      "row_count": 18
    },
    "rs_weights": {
      "path": "weights_rs_q1.csv",
      "checksum": "i9j0k1l2...",
      "row_count": 7
    }
  },
  "parameters": {
    "method": "sainte-lague",
    "normalize_weights": true
  },
  "outputs": {
    "prioritization_rs": "output/prioritization_rs.csv",
    "demand": "output/demand.csv",
    "metadata": "output/metadata.json"
  },
  "statistics": {
    "total_ideas": 247,
    "execution_time_seconds": 2.3,
    "warnings": 1,
    "errors": 0
  },
  "warnings": [
    "RA weights for eCommerce normalized from 98.5 to 100"
  ]
}

```
## 9.6 Security  
* **Input validation**: Prevent injection attacks via CSV  
* **File system**: Restricted to configured directories  
* **No remote execution**: All processing local  
* **Sensitive data**: No handling of PII or credentials  
* **Configuration security**: Validate all config parameters  
## 9.7 Scalability  
**Current Requirements** (v3.0):  
* Up to 1,000 IDEAs  
* Up to 50 Requesting Areas  
* Up to 10 Revenue Streams  
**Future Scalability** (v4.0+):  
* Up to 10,000 IDEAs  
* Up to 200 Requesting Areas  
* Parallel processing for multiple RSs  
* Database backend (optional)  
  
## 10. Implementation Roadmap  
## Phase 1: MVP (4 weeks)  
**Objectives**: Core functionality with Sainte-Laguë method  
**Deliverables**:  
* ✅ Data structures and validation  
* ✅ Sainte-Laguë algorithm (Level 2 and 3)  
* ✅ Basic CLI  
* ✅ CSV export for demand.csv  
* ✅ Unit tests (>70% coverage)  
* ✅ Basic documentation  
**Milestones**:  
* Week 1: Data model and validation  
* Week 2: Sainte-Laguë implementation  
* Week 3: CLI and integration  
* Week 4: Testing and documentation  
## Phase 2: Alternative Methods (2 weeks)  
**Objectives**: Add D'Hondt and WSJF methods  
**Deliverables**:  
* ✅ D'Hondt algorithm  
* ✅ WSJF algorithm  
* ✅ Method comparison functionality  
* ✅ Enhanced CLI with method selection  
* ✅ Comparison report export  
**Milestones**:  
* Week 5: D'Hondt implementation  
* Week 6: WSJF implementation and comparison  
## Phase 3: Usability Enhancements (2 weeks)  
**Objectives**: Improve user experience and validation  
**Deliverables**:  
* ✅ Advanced validation with clear error messages  
* ✅ Automatic weight normalization  
* ✅ Progress indicators  
* ✅ Enhanced logging  
* ✅ Configuration file support  
**Milestones**:  
* Week 7: Validation enhancements  
* Week 8: UX improvements  
## Phase 4: Integration and Analytics (3 weeks)  
**Objectives**: External integrations and reporting  
**Deliverables**:  
* 🔄 REST API for integration  
* 🔄 Webhook support for automated triggers  
* 🔄 Jira/Azure DevOps integration  
* 🔄 Dashboard for visualization (optional)  
* 🔄 Capacity planning report  
* 🔄 Historical trend analysis  
**Milestones**:  
* Week 9: API development  
* Week 10: Integration connectors  
* Week 11: Reporting and analytics  
**Legend**:  
* ✅ Included in v3.0  
* 🔄 Planned for v4.0  
  
## 11. Glossary  

| Term | Definition |
| ---------------------------- | -------------------------------------------------------------------- |
| IDEA | Development request created by a Requesting Area |
| Requesting Area (RA) | Direction/department responsible for creating and prioritizing IDEAs |
| Revenue Stream (RS) | Business revenue flow (e.g., eCommerce, Mail) |
| Revenue Stream Group (RSG) | Group of related Revenue Streams |
| Budget Group (BG) | Budget category (e.g., Technology, Operations) |
| Target Operating Model (TOM) | Organizational structure and delivery framework |
| WSJF | Weighted Shortest Job First - SAFe prioritization metric |
| Sainte-Laguë | Proportional allocation method using odd divisors |
| D'Hondt | Proportional allocation method using natural divisors |
| Quality Gate | Decision point between delivery phases |
| Quotient | Calculated value for determining proportional allocation |
| Seat | Metaphor for priority position in allocation algorithms |
| **MicroPhase (v3.1)** | Specific lifecycle stage from BusinessMap (e.g., "In Development", "Backlog") |
| **Queue (v3.1)** | Category for sequential prioritization (NOW, NEXT, or PRODUCTION) |
| **NOW Queue (v3.1)** | Highest priority queue containing IDEAs in Development phase (ranks 1-N) |
| **NEXT Queue (v3.1)** | Lower priority queue containing IDEAs in Planning phases (ranks N+1-M) |
| **PRODUCTION Queue (v3.1)** | No-priority queue for deployed IDEAs (no ranking) |
| **Sequential Ranking (v3.1)** | Ranking system where NOW items rank before NEXT items, enforcing "finish before start" |
| **Cost of Delay (CoD)** | Economic impact of delaying work |
| **Story Point (SP)** | Unit of effort estimation |
| **PI (Program Increment)** | Fixed timebox in SAFe (typically 8-12 weeks) |  
  
## 12. Appendices  
## Appendix A: Mathematical Formulas  
**A.1 Sainte-Laguë Quotient**  
$$Q_i = \frac{W_i}{2s_i + 1}$$  
Where:  
* $Q_i$ = Quotient for entity $i$  
* $W_i$ = Weight (votes) of entity $i$  
* $s_i$ = Number of seats already allocated to $i$  
**Divisor Sequence**: 1, 3, 5, 7, 9, 11, ...  
**A.2 D'Hondt Quotient**  
$$Q_i = \frac{W_i}{s_i + 1}$$  
Where:  
* $Q_i$ = Quotient for entity $i$  
* $W_i$ = Weight (votes) of entity $i$  
* $s_i$ = Number of seats already allocated to $i$  
**Divisor Sequence**: 1, 2, 3, 4, 5, 6, ...  
**A.3 WSJF Score**  
$$WSJF = \frac{CoD}{Size} = \frac{Value + Urgency + Risk}{Size}$$  
Where:  
* $CoD$ = Cost of Delay (Value + Urgency + Risk)  
* $Value$ = Business value (1-10)  
* $Urgency$ = Time criticality (1-10)  
* $Risk$ = Risk reduction (1-10)  
* $Size$ = Estimated effort (story points)  
**A.4 Adjusted WSJF (Level 2)**  
$$WSJF_{adjusted} = WSJF_{base} \times W_{RA}$$  
Where:  
* $WSJF_{base}$ = Base WSJF score of IDEA  
* $W_{RA}$ = Weight of the Requesting Area  
**A.5 Final WSJF (Level 3)**  
$$WSJF_{final} = WSJF_{adjusted} \times W_{RS}$$  
Where:  
* $WSJF_{adjusted}$ = Adjusted WSJF from Level 2  
* $W_{RS}$ = Weight of the Revenue Stream  
## Appendix B: Complete Execution Example  
**Scenario**: Small organization with 6 IDEAs, 2 RAs, 2 RSs  
**Input Files**:  
ideias.csv:  
```
ID,Name,RequestingArea,RevenueStream,BudgetGroup,PriorityRA,Value,Urgency,Risk,Size
I1,Portal,RA1,RS1,Technology,1,9,8,5,250
I2,Checkout,RA1,RS1,Commercial,2,7,9,3,100
I3,Analytics,RA2,RS1,Data&AI,1,8,7,6,140
I4,Sorting,RA3,RS2,Operations,1,8,10,7,300
I5,Tracking,RA3,RS2,Technology,2,6,8,5,200
I6,API,RA4,RS2,Technology,1,7,6,8,180

```
weights_ra.csv:  
```
RevenueStream,BudgetGroup,RequestingArea,Weight
RS1,Technology,RA1,60
RS1,Commercial,RA1,0
RS1,Data&AI,RA2,40
RS2,Operations,RA3,55
RS2,Technology,RA3,0
RS2,Technology,RA4,45

```
Note: RA can have weight in multiple BGs, summing their contribution  
weights_rs.csv:  
```
RevenueStream,Weight
RS1,60
RS2,40

```
**Execution**:  
```
python tom_demand.py prioritize \
  --ideas ideias.csv \
  --ra-weights weights_ra.csv \
  --rs-weights weights_rs.csv \
  --all-methods \
  --output-dir ./output/example

```
**Output - Level 2 (prioritization_rs.csv)**:  
```
RevenueStream,Method,Rank,ID,Name,RequestingArea,WSJF_Score
RS1,SainteLague,1,I1,Portal,RA1,0.088
RS1,SainteLague,2,I3,Analytics,RA2,0.150
RS1,SainteLague,3,I2,Checkout,RA1,0.190
RS1,DHondt,1,I1,Portal,RA1,0.088
RS1,DHondt,2,I2,Checkout,RA1,0.190
RS1,DHondt,3,I3,Analytics,RA2,0.150
RS1,WSJF,1,I2,Checkout,RA1,0.190
RS1,WSJF,2,I3,Analytics,RA2,0.150
RS1,WSJF,3,I1,Portal,RA1,0.088
RS2,SainteLague,1,I4,Sorting,RA3,0.083
RS2,SainteLague,2,I6,API,RA4,0.117
RS2,SainteLague,3,I5,Tracking,RA3,0.095
RS2,DHondt,1,I4,Sorting,RA3,0.083
RS2,DHondt,2,I5,Tracking,RA3,0.095
RS2,DHondt,3,I6,API,RA4,0.117
RS2,WSJF,1,I6,API,RA4,0.117
RS2,WSJF,2,I5,Tracking,RA3,0.095
RS2,WSJF,3,I4,Sorting,RA3,0.083

```
**Output - Level 3 (demand.csv)**:  
```
Method,GlobalRank,ID,Name,RequestingArea,RevenueStream,WSJF_Score
SainteLague,1,I1,Portal,RA1,RS1,0.088
SainteLague,2,I4,Sorting,RA3,RS2,0.083
SainteLague,3,I3,Analytics,RA2,RS1,0.150
SainteLague,4,I6,API,RA4,RS2,0.117
SainteLague,5,I2,Checkout,RA1,RS1,0.190
SainteLague,6,I5,Tracking,RA3,RS2,0.095
DHondt,1,I1,Portal,RA1,RS1,0.088
DHondt,2,I2,Checkout,RA1,RS1,0.190
DHondt,3,I4,Sorting,RA3,RS2,0.083
DHondt,4,I3,Analytics,RA2,RS1,0.150
DHondt,5,I5,Tracking,RA3,RS2,0.095
DHondt,6,I6,API,RA4,RS2,0.117
WSJF,1,I2,Checkout,RA1,RS1,0.190
WSJF,2,I3,Analytics,RA2,RS1,0.150
WSJF,3,I6,API,RA4,RS2,0.117
WSJF,4,I5,Tracking,RA3,RS2,0.095
WSJF,5,I1,Portal,RA1,RS1,0.088
WSJF,6,I4,Sorting,RA3,RS2,0.083

```
## Appendix C: Project Structure  
```
tom_demand_system/
├── src/
│   ├── __init__.py
│   ├── loader.py                 # Data loading functions
│   ├── validator.py              # Validation engine
│   ├── prioritizer.py            # Main prioritization logic
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── sainte_lague.py      # Sainte-Laguë implementation
│   │   ├── dhondt.py            # D'Hondt implementation
│   │   └── wsjf.py              # WSJF implementation
│   ├── exporter.py              # CSV export functions
│   ├── cli.py                   # Command-line interface
│   └── utils.py                 # Helper functions
│
├── tests/
│   ├── __init__.py
│   ├── test_loader.py           # Loader tests
│   ├── test_validator.py        # Validation tests
│   ├── test_algorithms.py       # Algorithm tests
│   ├── test_prioritizer.py      # Integration tests
│   ├── test_exporter.py         # Export tests
│   ├── test_cli.py              # CLI tests
│   └── fixtures/                # Test data
│       ├── ideias_test.csv
│       ├── weights_ra_test.csv
│       └── weights_rs_test.csv
│
├── config/
│   ├── config.yaml              # Default configuration
│   └── config.example.yaml      # Example configuration
│
├── data/
│   ├── input/                   # Input files directory
│   │   ├── ideias.csv
│   │   ├── weights_ra.csv
│   │   └── weights_rs.csv
│   └── output/                  # Output files directory
│       ├── prioritization_rs.csv
│       ├── demand.csv
│       └── metadata.json
│
├── docs/
│   ├── tom_demand.md            # This document
│   ├── api_reference.md         # API documentation
│   ├── user_guide.md            # User guide
│   └── examples/                # Example scenarios
│       └── quarterly_prioritization.md
│
├── scripts/
│   ├── setup.sh                 # Setup script
│   └── run_example.sh           # Run example scenario
│
├── .gitignore
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
├── README.md                    # Project README
└── LICENSE                      # License file

```
## Appendix D: Sample requirements.txt  
```
# Core dependencies
pandas>=1.3.0
numpy>=1.21.0
pyyaml>=5.4.0

# CLI enhancements
click>=8.0.0
colorama>=0.4.4
tqdm>=4.62.0

# Testing
pytest>=6.2.5
pytest-cov>=3.0.0
pytest-mock>=3.6.1

# Code quality
black>=21.9b0
flake8>=4.0.1
mypy>=0.910

# Documentation
sphinx>=4.2.0
sphinx-rtd-theme>=1.0.0

```
  
## 13. References  
## 13.1 Electoral Methods  
1. **Sainte-Laguë Method**:  
    * ++[Wikipedia: Webster/Sainte-Laguë method](https://en.wikipedia.org/wiki/Webster/Sainte-Lagu%C3%AB_method)++  
    * Used in: Norway, New Zealand, Sweden electoral systems  
    * Academic: Balinski, M.L., & Young, H.P. (1982). Fair Representation: Meeting the Ideal of One Man, One Vote  
2. **D'Hondt Method**:  
    * ++[Wikipedia: D'Hondt method](https://en.wikipedia.org/wiki/D%27Hondt_method)++  
    * Used in: European Parliament, many European countries  
    * Academic: Lijphart, A. (1994). Electoral Systems and Party Systems  
## 13.2 Agile and SAFe  
1. **WSJF (Weighted Shortest Job First)**:  
    * ++[Scaled Agile Framework: WSJF](https://scaledagileframework.com/wsjf/)++  
    * Reinertsen, D. G. (2009). The Principles of Product Development Flow  
2. **Lean Portfolio Management**:  
    * ++[SAFe: Lean Portfolio Management](https://scaledagileframework.com/lean-portfolio-management/)++  
    * Knaster, R., & Leffingwell, D. (2020). SAFe 5.0 Distilled  
## 13.3 Related Topics  
1. **Proportional Representation Theory**:  
    * Gallagher, M. (1991). Proportionality, Disproportionality and Electoral Systems  
2. **Portfolio Management**:  
    * Project Management Institute (2017). The Standard for Portfolio Management  
  
**End of Document**  
  
## Document Control  

| Version | Date | Author | Changes |
| ------- | ---------- | -------------- | ----------------------------------------------------------- |
| 1.0 | 2025-12-15 | LPM Specialist | Initial draft |
| 2.0 | 2026-01-01 | LPM Specialist | Added WSJF method |
| 3.0 | 2026-01-02 | LPM Specialist | Final version - English translation, complete specification |
  
**Approval**:  
* Portfolio Manager: _________________ Date: _______  
* CTO: _________________ Date: _______  
* Development Lead: _________________ Date: _______  
