# Analytics 2.0 – Solution Evolution

Analytics 2.0 was developed iteratively across **five major versions**.

The solution did not begin as a complete machine-learning system. Each version addressed a limitation or operational requirement identified during development and testing.

The evolution was:

```text
V1
Level 1 Categorization
        ↓
V2
Level 1 + Level 2 Hierarchical Categorization
        ↓
V3
Capability-Level Mapping
        ↓
V4
Whack-a-Mole (WAM) Analytics
        ↓
V5
Machine Learning Classification
```

---

# V1 – Level 1 Incident Categorization

## Objective

The first version focused on reducing the manual effort involved in categorizing incident records.

The goal was to analyze the incident `Description` field and automatically assign each incident to a broad **Level 1 category**.

## Approach

V1 used predefined keywords and regular-expression patterns.

```text
Incident Data
      ↓
Description
      ↓
Keyword / Regex Matching
      ↓
Level 1 Category
      ↓
Categorized Dataset
```

The classification rules were defined directly within the Python implementation.

Rules were evaluated sequentially, and once an incident received a valid category, later rules did not overwrite the classification.

Incidents that could not be matched were grouped separately for further analysis.

## Technologies

- Python
- Pandas
- NumPy
- Regular Expressions

## Key Achievement

V1 demonstrated that incident descriptions could be systematically converted into standardized high-level categories rather than relying entirely on manual categorization.

## Limitation

Level 1 classification provided only a broad understanding of the incident.

For example:

```text
Storage
Network
Database
Compute
```

More detailed classification was required to understand the specific type of issue occurring within each category.

This requirement led to **V2**.

---

# V2 – Level 1 & Level 2 Hierarchical Categorization

## Objective

V2 introduced more granular categorization and improved the scalability of the rule-processing framework.

The major improvements were:

- Level 1 categorization
- Level 2 sub-categorization
- Automated iterative mapping
- Externalized mapping logic
- Processing progress visibility using `tqdm`

## Hierarchical Classification

Instead of producing only:

```text
Storage
```

the solution could now produce a hierarchy such as:

```text
Storage
   ↓
Disk Capacity
```

Conceptually:

```text
Incident Description
        ↓
Level 1 Mapping
        ↓
Broad Category
        ↓
Level 2 Mapping
        ↓
Specific Issue Category
```

Level 2 classification depended on the Level 1 classification.

This prevented a Level 2 pattern belonging to one category from incorrectly classifying an incident belonging to another category.

## Automated Mapping

A major technical improvement in V2 was moving away from manually maintaining every mapping condition directly inside the Python logic.

Classification patterns were maintained in a mapping structure and Python iterated through those rules.

```text
Incident Data                Mapping Rules
      │                           │
      │                 ┌─────────┴─────────┐
      │                 │                   │
      │           Level 1 Rules       Level 2 Rules
      │                 │                   │
      └─────────────────┴─────────┬─────────┘
                                  ↓
                        Python Classification
                                  ↓
                         Level 1 + Level 2
```

This made the classification framework easier to maintain and extend.

## Large Dataset Processing

The solution was being executed against large incident datasets.

`tqdm` was introduced to provide execution progress while the classification rules were iterated.

Example:

```python
for row in tqdm(range(len(mapping_rules))):
    # Apply classification rule
```

This provided visibility into long-running classification processes during development and testing.

## Technologies

- Python
- Pandas
- NumPy
- Regular Expressions
- tqdm

## Key Achievement

V2 transformed the initial categorization prototype into a more reusable **hierarchical incident-classification framework**.

## Limitation

Although incidents could now be classified into detailed categories, analysis remained primarily focused on specific issue groups and smaller operational teams.

A broader ownership view was required so that leaders could understand issues across multiple teams under their responsibility.

This requirement led to **V3**.

---

# V3 – Capability-Level Mapping

## Objective

V3 introduced **capability-level mapping** on top of the existing Level 1 and Level 2 categorization.

The purpose was to provide broader operational visibility and ownership.

## Why Capability Mapping Was Needed

Until V2, the categorization framework helped identify detailed issue groups associated with smaller operational teams.

However, multiple teams could belong to the same broader technical capability.

Examples include:

```text
Network
Storage
Windows
Database
CloudOps
```

Instead of reviewing each smaller team independently, V3 introduced a higher-level capability view.

## Processing Flow

```text
Incident Data
      ↓
Level 1
      ↓
Level 2
      ↓
Team / Issue Group
      ↓
Capability Mapping
      ↓
Capability-Level Analytics
```

Conceptually:

```text
Multiple Operational Teams
          ↓
    Network Capability
          ↓
    Capability Leader
```

The same principle could be applied across Storage, Windows, Database, CloudOps and other capability groups.

> The capability names and mappings included in this public repository are generic examples. Original organizational structures and mappings are intentionally excluded.

## Business Improvement

V3 changed an important analytical question.

Earlier versions primarily helped answer:

> Which specific issue group or team is associated with this incident?

V3 additionally helped answer:

> Which broader capability owns the concentration of these issues?

This allowed capability leaders to review trends across the teams within their scope.

It also supported improvement discussions at the capability level instead of requiring improvement actions to be coordinated separately with numerous smaller teams.

## Technologies

- Python
- Pandas
- Level 1 / Level 2 classification
- Mapping tables
- Power BI analytics

## Key Achievement

V3 expanded Analytics 2.0 from an incident categorization framework into an **operational ownership and leadership analytics solution**.

## Limitation

Categorization and capability mapping explained where incidents were occurring.

The next requirement was to determine:

> Which issues are repeatedly occurring?

and:

> Are those issues getting better or worse?

This requirement led to **V4**.

---

# V4 – Whack-a-Mole (WAM) Analytics

## Objective

V4 introduced **Whack-a-Mole (WAM) Analytics** to identify repetitive incident patterns and analyze how those issues changed over time.

The goal was to move beyond:

> What incidents occurred?

toward:

> Which issues keep occurring, and are they improving or worsening?

## Issue Grouping

Recurring issues were analyzed using a combination of:

```text
Configuration Item + Level 2 Category
```

This helped identify repeated occurrences of similar issues against the same technical component.

## 30-Day Trend Analysis

WAM analyzed incident behavior across a **30-day observation window**.

The implementation compared:

```text
First 20 Days
      vs
Last 10 Days
```

Incident averages from these periods were used to determine how the issue was changing.

## Processing Flow

```text
Categorized Incident Data
          ↓
Configuration Item + Level 2
          ↓
Daily Incident Aggregation
          ↓
30-Day Observation Window
          ↓
┌────────────────────────────┐
│ First 20-Day Average       │
│             vs             │
│ Last 10-Day Average        │
└────────────────────────────┘
          ↓
Magnitude of Change
          ↓
Trend Classification
```

## Trend Outcomes

The analysis could identify conditions such as:

```text
Issue Increased
Issue Existing
Issue Decreasing
Issue Solved
```

This provided a simple way of distinguishing persistent or worsening issues from issues that were improving.

## Business Value

WAM enabled operational teams and capability leaders to:

- Identify repetitive issues
- Detect worsening incident patterns
- Prioritize problem areas
- Focus improvement activities on recurring problems
- Review whether improvement actions were reducing incident volumes

## Technologies

- Python
- Pandas
- Time-based aggregation
- Trend analysis
- Rule-based trend classification
- Power BI visualization

## Key Achievement

V4 added an **operational intelligence layer** to Analytics 2.0.

The solution could now:

```text
Categorize
     +
Assign Ownership
     +
Identify Repetition
     +
Analyze Trend Direction
```

## Limitation

The classification framework still relied significantly on predefined rules and mappings.

The next evolution explored whether historical categorized incidents could be used to automatically learn classification patterns.

This led to **V5**.

---

# V5 – Machine Learning Classification

## Objective

V5 introduced **supervised machine learning** for incident text classification.

Historical incident descriptions and their existing categories were used as labelled training data.

The goal was to train a model capable of predicting the appropriate category for new incident descriptions.

## Machine Learning Pipeline

```text
Historical Categorized Incidents
            ↓
       Data Cleaning
            ↓
Description + Category
            ↓
      Train/Test Split
            ↓
   TF-IDF Vectorization
            ↓
     Model Training
            ↓
     Model Evaluation
            ↓
   Best Model Selection
            ↓
    Category Prediction
```

## Text Vectorization

Incident descriptions are unstructured text.

Before applying machine-learning algorithms, the descriptions were transformed into numerical features using **TF-IDF (Term Frequency–Inverse Document Frequency)**.

The implementation considered both:

```text
Unigrams
+
Bigrams
```

Conceptually:

```text
"CPU utilization threshold exceeded"
                 ↓
           TF-IDF Vector
                 ↓
      Machine Learning Model
                 ↓
        Predicted Category
```

## Models Evaluated

Multiple classification algorithms were evaluated:

| Model | Mean Accuracy |
|---|---:|
| LinearSVC | 95% |
| Logistic Regression | 91% |
| Multinomial Naive Bayes | 81% |
| Random Forest Classifier | 50% |

**LinearSVC** produced the strongest result and was selected for the classification workflow.

## Why LinearSVC

TF-IDF produces a high-dimensional sparse representation of text.

LinearSVC is well suited to this type of text-classification problem and produced the strongest performance during the project evaluation.

## Model Persistence

After model selection, the trained components could be serialized for reuse.

```text
TF-IDF Vectorizer
        +
Trained Classification Model
        ↓
Reusable Prediction Pipeline
```

This allowed future incident descriptions to be processed using the same trained transformation and classification logic without rebuilding the complete training workflow for every prediction.

## Technologies

- Python
- Pandas
- scikit-learn
- TF-IDF
- LinearSVC
- Logistic Regression
- Multinomial Naive Bayes
- Random Forest
- Pickle

## Key Achievement

V5 extended Analytics 2.0 from a primarily rule-based analytics framework into a **machine-learning-assisted incident classification solution**.

---

# Complete Solution Evolution

The five development versions represent the progressive expansion of Analytics 2.0:

```text
┌─────────────────────────────────────┐
│ V1 – Level 1 Categorization         │
│ Keyword / Regex Classification      │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│ V2 – Level 1 + Level 2              │
│ Hierarchical & Automated Mapping    │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│ V3 – Capability Mapping             │
│ Leadership-Level Ownership View     │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│ V4 – WAM Analytics                  │
│ Repetitive Issue & Trend Detection  │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│ V5 – Machine Learning               │
│ Automated Text Classification       │
└─────────────────────────────────────┘
```

## Evolution at a Glance

| Version | Main Development | Primary Value |
|---|---|---|
| **V1** | Keyword/regex-based Level 1 mapping | Automated high-level categorization |
| **V2** | Level 1 + Level 2, automated mapping and `tqdm` | More granular and scalable categorization |
| **V3** | Capability-level mapping | Leadership-level visibility and ownership |
| **V4** | WAM repetitive issue analytics | Identification of recurring and changing issue patterns |
| **V5** | TF-IDF + supervised ML classification | Learned automated incident classification |

---

# From Categorization to Decision Support

The development journey can also be understood in terms of the questions each version enabled the solution to answer.

```text
V1
"What broad type of incident is this?"
        ↓
V2
"What specific type of issue is this?"
        ↓
V3
"Which capability should own and improve it?"
        ↓
V4
"Is this issue repeatedly occurring or getting worse?"
        ↓
V5
"Can historical data automatically predict the category?"
```

This iterative development approach allowed Analytics 2.0 to evolve from a simple categorization concept into a broader incident intelligence framework combining:

- Data preparation
- Rule-based text classification
- Hierarchical categorization
- Operational ownership mapping
- Repetitive issue analytics
- Trend analysis
- Power BI visualization
- Machine learning-based text classification

---

## Data Privacy

The original solution was developed using enterprise incident data.

For confidentiality and data-protection purposes, this public repository does **not** contain:

- Original incident datasets
- Customer or account information
- Internal organizational mappings
- Internal URLs or infrastructure paths
- Original Power BI datasets/files
- Production-trained ML models
- Confidential classification rules

All examples, mappings, identifiers and sample records included in this repository are sanitized or synthetic representations created solely to demonstrate the technical approach.
