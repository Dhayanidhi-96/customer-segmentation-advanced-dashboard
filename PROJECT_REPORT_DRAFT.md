# Customer Segmentation Platform - Project Report Draft

## Table of Contents

| S. No | Title | Page No |
|---|---|---|
| 1 | Introduction | 1 |
| 2 | System Configuration | 2 |
| 3 | Problem Statement | 3 |
| 4 | Literature Review | 4 |
| 5 | Objective | 5 |
| 6 | System Analysis | 6 |
| 6.1 | Existing System | 6 |
| 6.2 | Proposed System | 7 |
| 7 | Dataset Description | 8 |
| 8 | System Design | 9 |
| 8.1 | Architecture Diagram | 9 |
| 8.2 | ER Diagram | 10 |
| 8.3 | DFD (Data Flow Diagram) | 11 |
| 8.4 | Tools, Languages and Modules | 12 |
| 9 | Implementation | 13 |
| 10 | Results and Discussion | 16 |
| 11 | Testing | 19 |
| 11.1 | Unit Testing | 19 |
| 11.2 | Integration Testing | 20 |
| 11.3 | Performance Testing | 21 |
| 12 | Conclusion | 22 |
| 13 | Future Enhancement | 23 |
| 14 | References | 24 |
| 15 | Appendix - Source Code | 25 |

---

## 1. Introduction

Customer segmentation is a core strategy in modern e-commerce, enabling businesses to classify users based on behavioral and transactional patterns. This project presents a full-stack Customer Segmentation Platform that combines machine learning, real-time analytics, and campaign automation to support data-driven marketing decisions.

The platform is designed to handle large-scale customer datasets and provides interactive dashboards for monitoring key metrics such as customer distribution, revenue by segment, RFM trends, and model quality. It also supports campaign management and AI-assisted recommendations to improve engagement and retention.

---

## 2. System Configuration

### Hardware Configuration
- Processor: Intel Core i5 / i7 or equivalent
- RAM: Minimum 16 GB (recommended for large dataset training)
- Storage: SSD with at least 20 GB free space
- Network: Stable internet connection

### Software Configuration
- Operating System: Windows 10/11
- Python: 3.11
- Node.js: 18+
- PostgreSQL: 15+
- Redis: 7+
- Browser: Chrome / Edge (latest)
- Editor: VS Code

### Frameworks and Libraries
- Backend: FastAPI, SQLAlchemy, Pydantic
- Frontend: React, Vite, Recharts, React Query
- ML: scikit-learn, pandas, numpy, joblib
- Async: Celery

---

## 3. Problem Statement

E-commerce organizations often maintain huge customer datasets but fail to extract actionable segment-level insights in real time. Manual segmentation is slow, static, and unable to adapt to changing customer behavior.

The problem addressed in this project is to build a scalable platform that:
- Automatically segments customers using ML models,
- Compares model quality and selects the best model,
- Supports campaign execution by segment,
- Provides an easy-to-use dashboard for business users.

---

## 4. Literature Review

Several customer analytics systems focus only on static RFM scoring without dynamic model comparison. Research in clustering-based segmentation demonstrates that model quality can vary significantly with dataset size and feature engineering strategy.

Previous works highlight:
- K-Means as a strong baseline for segmentation,
- Gaussian Mixture for probabilistic assignments,
- RFM as an interpretable business metric,
- Need for combined evaluation metrics such as Silhouette, Davies-Bouldin, and Calinski-Harabasz.

This project extends these ideas into a practical end-to-end software platform.

---

## 5. Objective

The main objectives of this project are:
- Build a complete customer segmentation platform using modern web architecture.
- Train and evaluate multiple clustering models on customer behavioral data.
- Select and serve the best-performing model automatically.
- Enable campaign triggering and monitoring from a unified interface.
- Deliver fast dashboard performance for large datasets.

---

## 6. System Analysis

### 6.1 Existing System
- Segmentation often done in spreadsheets or static BI reports.
- Limited automation in model retraining and campaign flow.
- No integrated visualization with live operational controls.
- Weak scalability for large customer volumes.

### 6.2 Proposed System
- Centralized web platform with backend APIs and analytics dashboard.
- ML pipeline with automated model comparison and selection.
- Real-time and scheduled segmentation support.
- Campaign management module connected to segment outputs.
- Scalable processing flow for high-volume records.

---

## 7. Dataset Description

The dataset contains customer profile and order transaction data.

### Core Entities
- Customers: identity and demographic details
- Orders: purchase value, status, timestamp
- Segments: assigned label, RFM scores, model metadata

### Feature Engineering
- Recency
- Frequency
- Monetary
- Average order value
- Order consistency indicators
- Cancellation tendency

The platform supports large-scale synthetic dataset generation for testing and benchmarking.

---

## 8. System Design

### 8.1 Architecture Diagram

The system follows a layered architecture:
- Frontend (React dashboard)
- Backend API (FastAPI)
- Database (PostgreSQL)
- Cache/Queue (Redis + Celery)
- ML Engine (clustering pipeline)

### 8.2 ER Diagram

Main relationships:
- One customer can have many orders.
- One customer can have many segment history records.
- One customer can have many campaign records.
- Model run logs store training metadata.

### 8.3 DFD (Data Flow Diagram)

Key data flows:
1. Input customer and order data
2. Feature extraction and model training
3. Segment assignment and persistence
4. Dashboard consumption via APIs
5. Campaign trigger and execution lifecycle

### 8.4 Tools, Languages and Modules

- Languages: Python, JavaScript
- Backend: FastAPI, SQLAlchemy, Celery
- Frontend: React, Recharts
- Database: PostgreSQL
- ML: scikit-learn
- Modules: Customers, Segments, Analytics, Models, Campaigns, AI Advisor

---

## 9. Implementation

Implementation is divided into backend, frontend, and ML services.

### Backend
- REST endpoints for customer, segment, analytics, model, and campaign workflows
- ORM-based persistence and query optimization
- Async task support for background operations

### ML
- Preprocessing pipeline with feature scaling and dimensionality handling
- Multi-model training and score-based selection
- Artifact persistence and model-run tracking

### Frontend
- Interactive dashboard with KPI cards and charts
- Tab-based navigation for key modules
- Number formatting and performance-focused rendering for large records

---

## 10. Results and Discussion

The system successfully:
- Handles large customer datasets,
- Produces model ranking and best-model selection,
- Presents live metrics through visual components,
- Provides campaign control points for segment-specific actions.

Observed behavior indicates improved readability and usability with compact number formatting and chart payload control for large data volumes.

---

## 11. Testing

### 11.1 Unit Testing
- Individual utility and service functions validated.
- Formatting, preprocessing, and scoring logic checked for correctness.

### 11.2 Integration Testing
- API to database interactions validated.
- Frontend consumption of analytics endpoints verified.
- Background task trigger flow verified.

### 11.3 Performance Testing
- Large dataset training validated with optimized workflow.
- Dashboard endpoint load reduced through sampling and query optimization.
- UI responsiveness improved by limiting high-density chart payloads.

---

## 12. Conclusion

This project demonstrates a practical and scalable customer segmentation platform for e-commerce use cases. By combining ML, analytics visualization, and campaign orchestration, it enables faster and more reliable decision-making.

The system architecture supports extensibility, and current performance improvements make it suitable for high-volume data scenarios.

---

## 13. Future Enhancement

- Add advanced authentication and role-based access control.
- Introduce streaming updates with WebSocket channels.
- Add A/B testing workflows for campaign effectiveness.
- Add model explainability and drift monitoring.
- Introduce auto-scaling and distributed training options.

---

## 14. References

1. scikit-learn Documentation
2. FastAPI Documentation
3. SQLAlchemy Documentation
4. Recharts Documentation
5. Celery Documentation

---

## 15. Appendix - Source Code

### Main File
- backend/main.py
