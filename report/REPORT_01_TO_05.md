# Chapters 1 to 5

## Table Structure (As Requested)

| S. No | Title | Page No |
|---|---|---|
| 1 | Introduction | 1 |
| 2 | System Configuration | 3 |
| 3 | Problem Statement | 5 |
| 4 | Literature Review | 7 |
| 5 | Objective | 11 |

---

## 1. Introduction

### 1.1 Project Background

E-commerce platforms generate large volumes of customer transaction data every day. While this data is rich in business value, most organizations struggle to convert raw records into actionable segmentation strategies. Traditional approaches rely on static reports and manual business rules, which are often slow, inconsistent, and difficult to scale.

The Customer Segmentation Platform developed in this project addresses these challenges through a complete end-to-end system that combines:
- Data ingestion and management,
- Machine learning-based clustering,
- Segment analytics and visualization,
- Automated campaign orchestration,
- AI-powered recommendation support.

The platform is designed for practical business use, with a clean dashboard experience, robust backend services, and support for large datasets (tested up to 2.5 lakh customers).

### 1.2 Domain Context

Customer segmentation enables businesses to group users based on purchasing behavior and engagement quality. In this project, segmentation is based on both classical RFM logic and unsupervised clustering methods. The goal is to identify meaningful customer groups such as:
- VIP,
- Loyal,
- At-Risk,
- New,
- Churned,
- Potential.

Each segment can be targeted with specific campaign strategies, improving retention, conversion, and lifetime value.

### 1.3 Project Scope

The scope of this project includes:
- Building a full-stack analytics platform,
- Implementing multiple clustering models,
- Auto-selecting the best model using evaluation metrics,
- Displaying segment KPIs and visual charts,
- Supporting campaign trigger and execution tracking,
- Handling real-time and scheduled workflows.

Out-of-scope items include production-grade authentication, advanced MLOps orchestration pipelines, and enterprise observability integrations.

### 1.4 Key Contributions

This project contributes:
1. A working architecture for large-scale segmentation workflows.
2. A comparative ML training pipeline with model selection.
3. A dashboard optimized for high-volume data rendering.
4. A reusable campaign workflow integrated with segmentation output.
5. A modular codebase ready for future expansion.

### 1.5 Report Organization

This report is structured into 15 chapters covering conceptual basis, system design, implementation details, results, testing, and future enhancements.

---

## 2. System Configuration

### 2.1 Hardware Configuration

| Component | Minimum | Recommended |
|---|---|---|
| CPU | Intel i5 / Ryzen 5 | Intel i7 / Ryzen 7 |
| RAM | 8 GB | 16 GB or above |
| Storage | 10 GB free | SSD with 25 GB free |
| Network | Basic internet | Stable high-speed internet |

### 2.2 Software Configuration

| Layer | Technology |
|---|---|
| OS | Windows 10/11 |
| Frontend | React 18, Vite, Tailwind CSS |
| Backend | FastAPI (Python 3.11) |
| ORM | SQLAlchemy |
| Database | PostgreSQL 15 |
| Queue | Celery + Redis |
| ML | scikit-learn, pandas, numpy |
| Packaging | uv, npm |
| Reverse Proxy | Nginx |

### 2.3 Development Tools

| Tool | Usage |
|---|---|
| VS Code | Coding and debugging |
| Postman / Browser | API testing |
| Git | Version control |
| Docker (optional mode) | Containerized deployment |

### 2.4 Runtime Services

The project can be executed in two modes:
1. Manual localhost mode.
2. Docker-compose mode.

For local development, backend and frontend run independently while PostgreSQL and Redis provide persistent and queue infrastructure.

### 2.5 Environmental Variables

Essential environment variables include database credentials, Redis URL, API URLs, email provider keys, and AI provider keys. The project keeps all secrets in environment files to avoid hardcoding sensitive data.

---

## 3. Problem Statement

### 3.1 Core Problem

Businesses have customer and order data but cannot consistently answer:
- Who are the most valuable customers?
- Which users are likely to churn?
- Which campaign should be sent to whom and when?
- Which segmentation model is most reliable right now?

Without a structured segmentation platform, decisions become reactive and campaign ROI decreases.

### 3.2 Limitations in Current Practices

| Existing Practice | Limitation |
|---|---|
| Static reports | No real-time updates |
| Manual segmentation | Human bias and inconsistency |
| Single-model assumptions | No model quality comparison |
| Basic campaign blasts | Low personalization |
| Large exports to spreadsheets | Performance bottlenecks |

### 3.3 Need for Proposed System

A robust system is required that can:
1. Automatically compute behavior features.
2. Train and compare clustering models.
3. Assign segment labels with confidence.
4. Expose analytics through a fast dashboard.
5. Trigger campaigns and log outcomes.

---

## 4. Literature Review

### 4.1 Customer Segmentation Foundations

RFM analysis has been widely used in marketing analytics for ranking customer value through recency, frequency, and monetary dimensions. While RFM is simple and interpretable, it may miss complex behavior interactions. Modern segmentation combines RFM with machine learning clustering for better pattern discovery.

### 4.2 Clustering Methods in Marketing Analytics

#### K-Means
- Fast and scalable,
- Effective with compact spherical clusters,
- Sensitive to initialization and K selection.

#### DBSCAN
- Detects density-based clusters and outliers,
- No need to predefine K,
- Sensitive to parameter settings and scaling.

#### Hierarchical Agglomerative
- Generates hierarchical cluster relations,
- Useful for exploratory analysis,
- Computationally expensive for large datasets.

#### Gaussian Mixture Models
- Probabilistic clustering,
- Can model overlapping distributions,
- Higher computational cost compared to K-Means.

#### Spectral Clustering
- Good for non-linear boundaries,
- Expensive for large-scale datasets.

### 4.3 Model Evaluation Criteria

Common unsupervised metrics include:
- Silhouette Score (higher is better),
- Davies-Bouldin Index (lower is better),
- Calinski-Harabasz Score (higher is better).

A weighted composite can offer practical model ranking when metric scales differ.

### 4.4 Observations from Prior Work

1. No single model is universally best across all datasets.
2. Feature engineering quality often influences performance more than algorithm choice.
3. Large-scale deployments require query and rendering optimization, not just model tuning.
4. Operational integration (campaigns, dashboards, retraining) is often missing in academic prototypes.

### 4.5 Research Gap Addressed

This project addresses a practical gap: production-oriented integration of data pipeline, ML comparison, dashboard analytics, and campaign operations in one coherent platform.

---

## 5. Objective

### 5.1 Primary Objective

To develop a scalable customer segmentation platform that supports model-driven decision-making and campaign execution in a real-world e-commerce context.

### 5.2 Specific Objectives

1. Build modular backend APIs for customer, segment, analytics, model, and campaign workflows.
2. Implement a preprocessing and feature-engineering pipeline for customer behavior.
3. Train multiple clustering models and automatically select the best.
4. Provide dashboard views that remain responsive under high data volume.
5. Introduce campaign trigger and tracking capabilities.
6. Ensure maintainable architecture for future enhancements.

### 5.3 Success Criteria

| Objective | Measurement |
|---|---|
| Accurate segmentation | Stable cluster metrics and business-valid labels |
| Fast dashboard | Practical response times for major analytics endpoints |
| Campaign flow | Trigger, queue, and status tracking available |
| Scalability | Large dataset (up to 2.5 lakh customers) supported |
| Usability | Clear UI with readable compact number formats |

### 5.4 Deliverables

- Working source code (frontend + backend + ML + tasks),
- Configurable environment setup,
- Report documentation,
- Demonstrable analytics and model outputs.
