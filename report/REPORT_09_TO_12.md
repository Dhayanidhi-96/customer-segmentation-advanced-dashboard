# Chapters 9 to 12

## Table Structure (As Requested)

| S. No | Title | Page No |
|---|---|---|
| 9 | Implementation | 28 |
| 10 | Results and Discussion | 35 |
| 11 | Testing | 40 |
| 11.1 | Unit Testing | 40 |
| 11.2 | Integration Testing | 42 |
| 11.3 | Performance Testing | 44 |
| 12 | Conclusion | 47 |

---

## 9. Implementation

### 9.1 Backend Implementation

Backend is implemented using FastAPI with a modular route-service structure.

#### Router Modules

| Router | Key Endpoints |
|---|---|
| customers | list, detail, segment |
| segments | summary |
| analytics | dashboard, heatmap, scatter, revenue |
| models | list, best, retrain |
| emails | trigger, campaigns |
| ai | chat, recommendations |

#### Service Layer

| Service | Function |
|---|---|
| segmentation_service | real-time assignment using best model |
| email_service | email provider abstraction |
| grok_service | AI context and prompt orchestration |

### 9.2 ML Pipeline Implementation

The ML implementation includes:
1. Feature preprocessor,
2. Model adapters,
3. Evaluator,
4. Selector,
5. Training orchestrator.

#### Training Sequence

1. Build feature frame from transactional data.
2. Apply transforms and scaling.
3. Train candidate models.
4. Compute evaluation metrics.
5. Select best model and persist artifacts.
6. Assign segments and update current flags.

#### Large Data Optimizations Implemented

| Area | Optimization |
|---|---|
| Preprocessing | SQL aggregation instead of loading full ORM rows |
| Evaluation | Silhouette sampling to reduce memory pressure |
| Model training | Large-data mode using selected model subset |
| Segment updates | Batch inserts for assignment rows |

### 9.3 Frontend Implementation

Frontend is built with React + Vite and organized by pages/components/api hooks.

#### Main Tabs

- Dashboard
- Customers
- Segments
- Campaigns
- Models
- AI Advisor

#### Visualization Layer

Recharts components used for:
- Segment distribution,
- Revenue by segment,
- RFM heatmap,
- Scatter projection,
- Model comparison.

#### UX Improvements Implemented

1. Compact number formatting (K/L/Cr) with full value hints.
2. Simplified dashboard chart set for performance.
3. Model chart mode toggle (raw vs normalized).
4. Better campaign trigger feedback and status refresh.

### 9.4 Task Queue and Scheduling

Celery worker processes asynchronous jobs.
Celery beat schedules periodic jobs such as:
- model retraining,
- segmentation updates,
- campaign workflows.

### 9.5 Manual Localhost Deployment Flow

Core run sequence:
1. Configure env variables,
2. Seed data,
3. Train model,
4. Start backend,
5. Start worker and beat,
6. Start frontend.

(Refer to LOCALHOST_FLOW.md for command-level flow.)

---

## 10. Results and Discussion

### 10.1 Functional Results

| Feature | Status |
|---|---|
| Customer listing and detail | Working |
| Segment summary | Working |
| Dashboard charts | Working |
| Model training and best selection | Working |
| Campaign trigger and tracking | Working |

### 10.2 Model Results

The system successfully trained and selected best model on large dataset runs.

Observed best-model outputs include:
- model name,
- metric scores,
- training timestamp,
- artifact path.

### 10.3 Dashboard Behavior

Dashboard displays:
- total customer volume,
- monthly revenue,
- RFM indicator,
- email engagement,
- segment and revenue visual summaries.

Performance-focused chart simplification improved responsiveness under high data load.

### 10.4 Discussion

#### Positive Outcomes

1. End-to-end functionality from data to action.
2. Better readability through compact unit display.
3. Improved scale handling via backend query optimization.
4. Usable model comparison after adding chart modes.

#### Limitations

1. Advanced campaign outcome analytics can be expanded.
2. More model diversity can be restored with distributed compute.
3. Security/authentication layer is basic for demo context.

---

## 11. Testing

### 11.1 Unit Testing

#### Scope

- Utility formatters,
- Feature calculation helpers,
- Model score utilities,
- Endpoint schema responses.

#### Sample Unit Test Matrix

| Test ID | Module | Input | Expected |
|---|---|---|---|
| UT-01 | number formatter | 250000 | 2.5L |
| UT-02 | currency formatter | 47000000 | ₹4.7Cr |
| UT-03 | evaluator | valid label set | metric dict returned |
| UT-04 | preprocessor | empty dataset | empty frame |

### 11.2 Integration Testing

#### API Integration Cases

| Test ID | Endpoint | Expected Outcome |
|---|---|---|
| IT-01 | /api/health | status ok |
| IT-02 | /api/models/best | best model payload |
| IT-03 | /api/segments/summary | segment counts and revenue |
| IT-04 | /api/emails/campaigns | campaign stats and list |

#### Frontend Integration Cases

| Test ID | UI Tab | Expected Outcome |
|---|---|---|
| IT-05 | Dashboard | charts load with data |
| IT-06 | Models | toggle raw/normalized works |
| IT-07 | Campaigns | trigger feedback visible |

### 11.3 Performance Testing

#### Performance Goals

| Metric | Goal |
|---|---|
| Dashboard first render | Practical interactive response |
| Large data training | Completes without memory crash |
| Segment summary endpoint | Low-latency grouped response |

#### Observed Improvements

1. Reduced N+1 queries in summary endpoints.
2. Reduced scatter payload through sampling limit.
3. Reduced model-evaluation memory via metric sampling.
4. Increased frontend smoothness with cache tuning.

---

## 12. Conclusion

This project demonstrates a practical, scalable customer segmentation platform with integrated ML, analytics, and campaign operations.

Key achievements:
1. Full-stack implementation from data layer to dashboard.
2. Successful large-data segmentation workflow.
3. Business-oriented readability and usability improvements.
4. Modular structure suitable for iterative enhancement.

The resulting system serves both technical and business users, enabling faster segmentation insight and action cycles.
