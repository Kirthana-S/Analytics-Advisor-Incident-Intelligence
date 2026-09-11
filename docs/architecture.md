# Analytics 2.0 – Solution Architecture

## Architecture Overview

Analytics 2.0 is an incident intelligence and analytics solution designed to transform raw incident records into standardized categories, operational insights, repetitive issue trends, and machine-learning-assisted classifications.

The architecture evolved across multiple development versions but can be represented as an end-to-end analytics pipeline.

```text
┌──────────────────────────────┐
│     Incident Data Source     │
│                              │
│ Description                  │
│ Configuration Item           │
│ Support / Assignment Group   │
│ Created Date                 │
│ Other Incident Attributes    │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│   Data Preparation Layer     │
│                              │
│ • Data cleaning              │
│ • Duplicate handling         │
│ • Missing-value handling     │
│ • Text preparation           │
│ • Date preparation           │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Classification Layer         │
│                              │
│ Level 1 Categorization       │
│          ↓                   │
│ Level 2 Categorization       │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Operational Mapping Layer    │
│                              │
│ Capability Mapping           │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Incident Intelligence Layer  │
│                              │
│ WAM Analytics                │
│ Repetitive Issue Detection   │
│ 30-Day Trend Analysis        │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Analytics & Visualization    │
│                              │
│ Power BI                     │
│ KPI Analysis                 │
│ Trend Analysis               │
│ Capability Views             │
│ Drill-Down Analysis          │
└──────────────────────────────┘
```

---

# 1. Data Input Layer

The solution starts with structured incident records.

Relevant fields used across the different stages of the solution included information such as:

```text
Incident Identifier
Description
Configuration Item
Assignment / Working Group
Created Date
Closed Date
Other Operational Attributes
```

The incident `Description` field is particularly important because it provides the unstructured text used for rule-based and machine-learning classification.

> Original datasets are not included in this repository. Public examples use synthetic incident records.

---

# 2. Data Preparation Layer

Before classification and analysis, the incident dataset is prepared using Python and Pandas.

Typical preparation activities include:

- Removing duplicate incident records
- Handling missing values
- Cleaning description text
- Removing unnecessary line breaks
- Standardizing required fields
- Converting date columns into appropriate datetime formats

Conceptually:

```text
Raw Incident Dataset
        ↓
Data Quality Checks
        ↓
Cleaning
        ↓
Text Preparation
        ↓
Date Preparation
        ↓
Analytics-Ready Dataset
```

The purpose of this stage is to create a consistent dataset for the downstream classification and analytics processes.

---

# 3. Rule-Based Classification Layer

The initial classification architecture uses predefined patterns to analyze incident descriptions.

## Level 1 Classification

Level 1 represents the broader incident category.

```text
Incident Description
        ↓
Keyword / Regex Rules
        ↓
Level 1
```

Example:

```text
"Disk space threshold exceeded"
        ↓
Storage
```

## Level 2 Classification

Level 2 provides more detailed classification within the assigned Level 1 category.

```text
Incident Description
        +
Assigned Level 1
        ↓
Level 2 Rules
        ↓
Level 2
```

Example:

```text
Level 1 : Storage
Level 2 : Disk Capacity
```

The Level 2 mapping is dependent on Level 1, helping maintain a hierarchical classification structure.

---

# 4. Configuration-Driven Mapping

As the solution evolved, classification rules were separated from the core processing logic.

Conceptually:

```text
                 ┌───────────────────┐
                 │ Level 1 Rules     │
                 └─────────┬─────────┘
                           │
Incident Data ─────────────┼──────→ Classification Engine
                           │
                 ┌─────────┴─────────┐
                 │ Level 2 Rules     │
                 └───────────────────┘
```

This design makes the classification logic more reusable because mappings can be updated without redesigning the complete processing workflow.

The public repository demonstrates this architecture using synthetic configuration files.

---

# 5. Capability Mapping Layer

After detailed categorization, incidents can be mapped into broader operational capabilities.

```text
Level 1
   +
Level 2
   +
Operational Mapping
        ↓
Capability
```

Example capability groups represented in the public implementation include:

```text
Network
Storage
Windows
Database
CloudOps
```

Capability mapping provides a higher-level analytical view across multiple operational teams.

```text
Detailed Operational Groups
           ↓
      Capability
           ↓
 Capability-Level View
```

This allows the output to support both detailed incident analysis and broader leadership-level analysis.

---

# 6. WAM Analytics Layer

Whack-a-Mole (WAM) Analytics is used to identify repetitive issues and understand whether those issues are improving or worsening.

The primary analytical combination is:

```text
Configuration Item + Level 2
```

Incident occurrences are analyzed across a 30-day period.

```text
30-Day Incident Window
          ↓
┌─────────────────────────┐
│ First 20 Days           │
│ Average Incident Volume │
└────────────┬────────────┘
             │
             │ Compare
             │
┌────────────┴────────────┐
│ Last 10 Days            │
│ Average Incident Volume │
└────────────┬────────────┘
             ↓
     Magnitude of Change
             ↓
       Trend Status
```

Possible trend outputs include:

```text
Issue Increased
Issue Existing
Issue Decreasing
Issue Solved
```

This layer converts categorized incident data into actionable trend information.

---

# 7. Machine Learning Classification Layer

The machine-learning component provides an additional classification approach based on historical labelled incident data.

```text
Historical Incident Data
          ↓
Description + Category
          ↓
Train / Test Split
          ↓
TF-IDF Vectorization
          ↓
Machine Learning Models
```

The evaluated models included:

```text
LinearSVC
Logistic Regression
Multinomial Naive Bayes
Random Forest Classifier
```

Project evaluation identified LinearSVC as the strongest-performing model.

The trained workflow can conceptually be represented as:

```text
New Incident Description
          ↓
Trained TF-IDF Vectorizer
          ↓
Numerical Feature Vector
          ↓
Trained LinearSVC
          ↓
Predicted Incident Category
```

The machine-learning layer therefore complements the rule-based classification framework by learning categorization patterns from historical data.

---

# 8. Power BI Analytics Layer

The processed output can be consumed by Power BI for operational analytics and visualization.

The visualization layer supports views such as:

- Incident category distribution
- Level 1 trends
- Level 2 trends
- Capability-level incident analysis
- Repetitive issue analysis
- WAM trend status
- KPI monitoring
- Drill-down analysis

Conceptually:

```text
Python Processing
        ↓
Enriched Incident Dataset
        ↓
Power BI Data Model
        ↓
Dashboards / KPIs / Trends
        ↓
Operational Insights
```

Power BI acts as the presentation and decision-support layer of the solution.

---

# 9. End-to-End Architecture

The complete solution architecture can therefore be summarized as:

```text
                        INCIDENT DATA
                              │
                              ▼
                    ┌──────────────────┐
                    │ Data Preparation │
                    │ Python + Pandas  │
                    └────────┬─────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Rule Classification  │
                  │                      │
                  │ Level 1 → Level 2    │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Capability Mapping   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ WAM Analytics        │
                  │                      │
                  │ Repetitive Issues    │
                  │ Trend Detection      │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Enriched Analytics   │
                  │ Dataset              │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Power BI             │
                  │                      │
                  │ Dashboards           │
                  │ KPIs                 │
                  │ Trends               │
                  │ Capability Insights  │
                  └──────────────────────┘


             MACHINE LEARNING EXTENSION

              Historical Categorized Data
                         │
                         ▼
                       TF-IDF
                         │
                         ▼
                  Model Evaluation
                         │
                         ▼
                     LinearSVC
                         │
                         ▼
              Predicted Classification
```

---

# 10. Technology Stack

| Layer | Technologies / Techniques |
|---|---|
| Data Processing | Python, Pandas, NumPy |
| Text Processing | Regex, TF-IDF |
| Classification | Rule-based mapping, hierarchical classification |
| Progress Monitoring | tqdm |
| Operational Analytics | Capability mapping, WAM |
| Machine Learning | scikit-learn |
| ML Algorithms | LinearSVC, Logistic Regression, MultinomialNB, Random Forest |
| Visualization | Power BI |
| Model Persistence | Pickle |

---

# 11. Architecture Evolution

The architecture was not designed as a single final implementation from the beginning.

It evolved progressively:

```text
V1
Rule-Based Level 1 Mapping
        ↓
V2
Hierarchical Level 1 + Level 2 Mapping
        ↓
V3
Capability Mapping
        ↓
V4
WAM Trend Analytics
        ↓
V5
Machine Learning Classification
```

This iterative architecture allowed each development version to address a specific limitation discovered during implementation and testing.

---

# Data Privacy & Public Repository Design

This repository demonstrates the technical architecture without exposing the original enterprise environment.

The following are intentionally excluded:

- Original incident data
- Customer/account names
- Internal team names
- Internal organizational mappings
- Internal URLs
- Local/internal file paths
- Production regex mappings
- Original Power BI files
- Production-trained ML models
- Other confidential organizational information

Synthetic datasets and generic mappings are used wherever examples are required.
