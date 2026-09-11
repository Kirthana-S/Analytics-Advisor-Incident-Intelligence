# V5 – Machine Learning Classification

## Objective

Version 5 introduced machine learning to reduce dependence on manually configured classification rules.

Historical incident descriptions and their previously assigned categories were used as labelled training data.

The objective was to train a model capable of predicting the category of new incident descriptions.

## Machine Learning Pipeline

```text
Historical Categorized Incidents
        ↓
Data Cleaning
        ↓
Description + Category
        ↓
Train / Test Split
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
