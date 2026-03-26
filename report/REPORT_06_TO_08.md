# Chapters 6 to 8

## Table Structure (As Requested)

| S. No | Title | Page No |
|---|---|---|
| 6 | System Analysis | 12 |
| 6.1 | Existing System | 12 |
| 6.2 | Proposed System | 14 |
| 7 | Dataset Description | 17 |
| 8 | System Design | 20 |
| 8.1 | Architecture Diagram | 20 |
| 8.2 | ER Diagram | 22 |
| 8.3 | DFD (Data Flow Diagram) | 24 |
| 8.4 | Tools, Languages and Modules | 26 |

---

## 6. System Analysis

### 6.1 Existing System

Existing segmentation and campaign workflows in many organizations are fragmented across spreadsheets, BI tools, CRM exports, and manual communication processes.

#### Existing Workflow Characteristics

| Area | Existing Approach | Challenge |
|---|---|---|
| Data Preparation | Manual exports and cleaning | Time-consuming and error-prone |
| Segmentation | Static rule-based grouping | Limited adaptability |
| Model Usage | Rarely applied in operations | No continuous optimization |
| Reporting | Periodic dashboards | Not real-time |
| Campaigning | Batch sends | Weak personalization |

#### Pain Points

1. Data freshness problem:
   - Segment definitions quickly become outdated when buying behavior changes.

2. Traceability problem:
   - Hard to know which model/rule produced a segment assignment.

3. Scalability problem:
   - Spreadsheets and unoptimized reports fail at high customer volume.

4. Operational gap:
   - Analytics and campaign execution are disconnected.

5. Decision delay:
   - Teams spend more time preparing data than acting on insights.

### 6.2 Proposed System

The proposed system unifies all major workflow layers into one platform:
- Data persistence,
- Feature engineering,
- Model training and selection,
- Segment assignment,
- Analytics visualization,
- Campaign trigger and tracking.

#### Proposed System Highlights

| Capability | Proposed Solution |
|---|---|
| Feature Engineering | Automated RFM + behavioral feature extraction |
| Model Training | Multi-model pipeline with score-based selection |
| Scalability | Query optimization and payload control |
| Dashboard UX | Fast charts + compact number readability |
| Campaign Integration | Trigger and status logs tied to segments |

#### Functional Benefits

1. Real-time operational visibility.
2. Better campaign targeting precision.
3. Clear model governance via model-run logs.
4. Flexible retraining and future extensibility.

#### Non-Functional Benefits

- Maintainability through modular architecture,
- Performance improvements for large datasets,
- Better user clarity with explicit units and chart simplification.

---

## 7. Dataset Description

### 7.1 Data Sources

The platform uses relational transactional data:
- `customers` table,
- `orders` table,
- derived segmentation and model metadata tables.

### 7.2 Core Customer Schema

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique customer identifier |
| email | VARCHAR | Primary email |
| name | VARCHAR | Full name |
| phone | VARCHAR | Contact number |
| country/city | VARCHAR | Geography |
| age/gender | INT/VARCHAR | Demographics |
| is_active | BOOLEAN | Active account status |

### 7.3 Order Schema

| Field | Type | Description |
|---|---|---|
| id | UUID | Order identifier |
| customer_id | UUID | FK to customer |
| order_number | VARCHAR | Business order key |
| amount | DECIMAL | Transaction amount |
| items_count | INT | Total items |
| status | ENUM | completed/cancelled/refunded |
| created_at | DATETIME | Order timestamp |

### 7.4 Engineered Features

| Feature | Description |
|---|---|
| recency_days | Days since latest purchase |
| frequency | Number of orders |
| monetary | Total spend |
| avg_order_value | Mean spend per order |
| order_std_dev | Spending variability |
| days_between_orders | Average purchase gap |
| cancellation_rate | Cancelled / total orders |

### 7.5 Data Scale

The platform supports small and large seed sizes. In current validation, large-scale training was executed at:
- 250,000 customers,
- large order volume generated across profiles.

### 7.6 Segment Labels

Business segment labels used:
- VIP,
- Loyal,
- At-Risk,
- New,
- Churned,
- Potential,
- Outlier.

### 7.7 Data Quality Controls

1. Null-safe aggregation defaults.
2. Log transform for skewed fields.
3. Scaled features for clustering stability.
4. Controlled synthetic profile distributions.

---

## 8. System Design

### 8.1 Architecture Diagram

**Insert Figure 8.1: System Architecture Diagram**

Recommended diagram blocks:
1. React Frontend (Dashboard, Tabs, Charts)
2. FastAPI Backend (Routers + Services)
3. ML Layer (Preprocessing + Models + Selector)
4. PostgreSQL Database
5. Redis + Celery (Worker + Beat)
6. External Services (Email Provider, AI Provider)

#### Architecture Narrative

Frontend requests data from backend APIs. Backend services query PostgreSQL and orchestrate ML workflows. Celery executes asynchronous/scheduled tasks for campaigns and retraining. Model artifacts are persisted and used by segmentation services.

### 8.2 ER Diagram

**Insert Figure 8.2: ER Diagram**

Main entities:
- customers
- orders
- customer_segments
- email_campaigns
- model_runs
- grok_sessions

Relationships:
1. Customer 1..* Orders
2. Customer 1..* CustomerSegments
3. Customer 1..* EmailCampaigns
4. ModelRuns logs are independent run metadata

### 8.3 DFD (Data Flow Diagram)

**Insert Figure 8.3: Level-0 DFD**

External actors:
- Admin/User
- Email Service
- AI Service

Processes:
1. Customer Data Processing
2. Model Training and Selection
3. Segment Assignment
4. Analytics Rendering
5. Campaign Triggering

Data stores:
- PostgreSQL
- Model Artifacts

**Insert Figure 8.4: Level-1 DFD for Training Pipeline**

### 8.4 Tools, Languages and Modules

#### Tools and Languages

| Category | Stack |
|---|---|
| Backend | Python, FastAPI, SQLAlchemy |
| Frontend | JavaScript, React, Vite |
| Database | PostgreSQL |
| Queue | Redis, Celery |
| ML | scikit-learn, pandas, numpy |
| Build | npm, uv |

#### Module Breakdown

| Module | Responsibility |
|---|---|
| Customers | List/detail/re-segmentation |
| Segments | Summary and segment-level analytics |
| Analytics | Dashboard KPI + chart APIs |
| Models | Retraining, best-model, run history |
| Campaigns | Trigger and campaign tracking |
| AI Advisor | Context-based recommendations |

#### Design Principles

1. Separation of concerns between routers/services/ML.
2. Async background processing for heavy operations.
3. Scalable query patterns for high data volume.
4. UI clarity via compact units and explicit labels.
