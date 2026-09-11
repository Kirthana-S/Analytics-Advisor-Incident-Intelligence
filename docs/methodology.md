# Analytics 2.0 – Methodology

## Overview

Analytics 2.0 followed an iterative data analytics and machine learning methodology for transforming raw incident records into structured operational insights.

The overall methodology consisted of:

```text
Data Collection
      ↓
Data Preparation
      ↓
Rule-Based Classification
      ↓
Hierarchical Categorization
      ↓
Capability Mapping
      ↓
Repetitive Issue Analysis
      ↓
Machine Learning
      ↓
Power BI Visualization
      ↓
Validation & Iterative Improvement
```

---

# 1. Data Preparation

The first stage focused on preparing incident records for analysis.

Key activities included:

- Selecting relevant incident attributes
- Removing duplicate records
- Handling missing values
- Cleaning incident descriptions
- Removing unnecessary line breaks and text artifacts
- Converting date fields into usable datetime formats
- Preparing structured data for downstream processing

The `Description` field was particularly important because it contained the text used for incident categorization.

```text
Raw Incident Data
        ↓
Cleaning
        ↓
Standardization
        ↓
Analytics-Ready Dataset
```

---

# 2. Rule-Based Text Categorization

The initial classification approach used keywords and regular expressions to identify patterns within incident descriptions.

```text
Incident Description
        ↓
Keyword / Regex Pattern
        ↓
Matched Rule
        ↓
Assigned Category
```

This provided a deterministic baseline for automated categorization.

Rules were processed sequentially, with valid earlier classifications protected from unnecessary overwriting.

---

# 3. Hierarchical Classification

The categorization methodology was expanded into two levels.

```text
Description
     ↓
Level 1
     ↓
Level 2
```

**Level 1** represented the broader issue category.

**Level 2** represented a more specific issue within the Level 1 category.

For Level 2 classification, both conditions were considered:

```text
Correct Level 1
       +
Level 2 Regex Match
       ↓
Level 2 Category
```

This reduced the possibility of assigning a detailed issue category outside its intended parent category.

---

# 4. Configuration-Driven Rule Processing

As the classification framework expanded, mapping rules were separated from the core Python processing logic.

Instead of maintaining every condition directly inside the program:

```text
Mapping Configuration
        ↓
Python Iteration
        ↓
Rule Evaluation
        ↓
Category Assignment
```

This improved maintainability and allowed classification rules to be extended without redesigning the processing workflow.

`tqdm` was used to monitor progress during iterative processing of larger datasets.

---

# 5. Capability Mapping

After hierarchical categorization, incidents were mapped to broader operational capabilities.

```text
Detailed Classification
        ↓
Operational Mapping
        ↓
Capability
```

This enabled analysis at multiple levels:

```text
Detailed Issue View
        +
Capability-Level View
```

The capability layer supported broader operational ownership and leadership analysis across multiple smaller teams.

---

# 6. Repetitive Issue Analysis – WAM

Whack-a-Mole (WAM) analytics was introduced to identify recurring issues and analyze their direction over time.

Incidents were analyzed using:

```text
Configuration Item + Level 2
```

The methodology used a 30-day observation window.

```text
First 20 Days
      ↓
Average Incident Volume

          VS

Last 10 Days
      ↓
Average Incident Volume
```

The difference between these periods was used to calculate the magnitude of change.

Based on the resulting trend, issues could be classified into states such as:

```text
Issue Increased
Issue Existing
Issue Decreasing
Issue Solved
```

This methodology helped distinguish isolated incidents from persistent or changing operational problems.

---

# 7. Machine Learning Methodology

The final development stage explored supervised machine learning for incident text classification.

Historical categorized incidents provided the labelled dataset.

## Feature and Target

```text
Feature (X)
Incident Description

Target (y)
Incident Category
```

## TF-IDF Feature Extraction

Incident descriptions were transformed into numerical features using TF-IDF.

```text
Incident Description
        ↓
TF-IDF Vectorizer
        ↓
Numerical Feature Matrix
```

The implementation used both unigrams and bigrams to represent useful textual patterns.

---

# 8. Model Training & Evaluation

Multiple classification algorithms were evaluated:

- LinearSVC
- Logistic Regression
- Multinomial Naive Bayes
- Random Forest Classifier

The project evaluation produced:

| Model | Mean Accuracy |
|---|---:|
| LinearSVC | 95% |
| Logistic Regression | 91% |
| Multinomial Naive Bayes | 81% |
| Random Forest Classifier | 50% |

LinearSVC produced the strongest result and was selected for the classification workflow.

The methodology can be summarized as:

```text
Historical Labelled Data
        ↓
Train / Test Preparation
        ↓
TF-IDF
        ↓
Model Training
        ↓
Model Evaluation
        ↓
Model Comparison
        ↓
Best Model Selection
        ↓
LinearSVC
```

---

# 9. Model Reuse

After training and model selection, the trained classification components could be serialized for reuse.

```text
Trained TF-IDF Vectorizer
          +
Trained Classification Model
          ↓
Saved Model Components
          ↓
Future Classification
```

This allowed new incident descriptions to be transformed and classified using the trained workflow.

---

# 10. Visualization & Analysis

Processed and enriched incident data was used for Power BI analysis.

The visualization methodology focused on converting technical classification output into operational insights.

Analysis included areas such as:

- Incident volumes
- Category distributions
- Level 1 / Level 2 trends
- Capability trends
- Repetitive issue patterns
- WAM status
- Operational KPIs
- Drill-down analysis

Conceptually:

```text
Python Processing
       ↓
Enriched Dataset
       ↓
Power BI
       ↓
Visual Analysis
       ↓
Operational Insights
```

---

# 11. Iterative Development Methodology

A key characteristic of Analytics 2.0 was iterative development.

Each version addressed limitations identified in the previous implementation.

```text
V1
Broad Categorization
        ↓
Need More Detail

V2
Hierarchical Categorization
        ↓
Need Broader Ownership

V3
Capability Mapping
        ↓
Need Repetitive Issue Intelligence

V4
WAM Analytics
        ↓
Need Learned Classification

V5
Machine Learning
```

Development therefore followed a continuous cycle:

```text
Develop
   ↓
Test
   ↓
Validate
   ↓
Identify Limitation
   ↓
Improve
   ↓
Retest
```

---

# 12. Tools & Techniques

| Area | Tools / Techniques |
|---|---|
| Data Preparation | Python, Pandas, NumPy |
| Text Processing | Regex |
| Rule Processing | Python loops, configuration tables |
| Processing Visibility | tqdm |
| Hierarchical Classification | Level 1 + Level 2 mapping |
| Operational Mapping | Capability mapping |
| Repetitive Issue Analysis | WAM |
| Feature Engineering | TF-IDF |
| Machine Learning | scikit-learn |
| Model Evaluation | Accuracy comparison |
| Selected ML Model | LinearSVC |
| Model Persistence | Pickle |
| Visualization | Power BI |

---

# 13. Public Repository Methodology

The public implementation preserves the methodology and technical concepts of the original project while protecting confidential information.

Therefore:

- Production incident records are not published.
- Customer/account information is excluded.
- Internal team mappings are excluded.
- Internal URLs and file paths are excluded.
- Original production regex mappings are excluded.
- Production-trained models are excluded.
- Synthetic examples are used to demonstrate the workflow.

This allows the repository to demonstrate the project's technical methodology without exposing confidential enterprise information.
