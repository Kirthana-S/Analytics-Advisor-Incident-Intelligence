"""
Analytics 2.0 - Version 5
Machine Learning Based Incident Classification

Purpose:
Train and evaluate multiple text-classification models using
historical incident descriptions and select the best-performing model.

The public version uses synthetic sample data only.
Production datasets and organizational identifiers are excluded.
"""

import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC


def prepare_data(df: pd.DataFrame):
    """
    Prepare incident descriptions and target labels.
    """

    data = df.copy()

    data = data.dropna(
        subset=["Description", "Category"]
    )

    X = data["Description"]
    y = data["Category"]

    return X, y


def split_data(X, y):
    """
    Split data into training and testing datasets.
    """

    return train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )


def vectorize_text(
    X_train,
    X_test,
):
    """
    Convert incident descriptions into TF-IDF features.
    """

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        stop_words="english",
    )

    X_train_tfidf = vectorizer.fit_transform(
        X_train
    )

    X_test_tfidf = vectorizer.transform(
        X_test
    )

    return (
        vectorizer,
        X_train_tfidf,
        X_test_tfidf,
    )


def evaluate_models(
    X_train,
    X_test,
    y_train,
    y_test,
):
    """
    Train and compare multiple classification models.
    """

    models = {
        "LinearSVC": LinearSVC(),
        "LogisticRegression": LogisticRegression(
            max_iter=1000
        ),
        "MultinomialNB": MultinomialNB(),
        "RandomForestClassifier":
            RandomForestClassifier(
                random_state=42
            ),
    }

    results = {}

    for name, model in models.items():

        model.fit(
            X_train,
            y_train,
        )

        predictions = model.predict(
            X_test
        )

        accuracy = accuracy_score(
            y_test,
            predictions,
        )

        results[name] = {
            "model": model,
            "accuracy": accuracy,
        }

    return results


def select_best_model(results):
    """
    Select the model with the highest accuracy.
    """

    best_model_name = max(
        results,
        key=lambda name:
            results[name]["accuracy"],
    )

    return (
        best_model_name,
        results[best_model_name]["model"],
    )


def save_model(
    vectorizer,
    model,
):
    """
    Serialize the trained vectorizer and model.
    """

    with open(
        "tfidf_vectorizer.pkl",
        "wb",
    ) as file:
        pickle.dump(
            vectorizer,
            file,
        )

    with open(
        "incident_classifier.pkl",
        "wb",
    ) as file:
        pickle.dump(
            model,
            file,
        )


if __name__ == "__main__":

    # Synthetic training data
    sample_data = pd.DataFrame(
    {
        "Description": [
            # CPU
            "CPU utilization threshold exceeded",
            "Processor load is very high",
            "CPU usage remains above threshold",
            "High processor utilization detected",

            # Storage
            "Disk space threshold exceeded",
            "Filesystem running out of space",
            "Available disk capacity is low",
            "Storage volume nearing capacity",

            # Network
            "Network connectivity unavailable",
            "Unable to reach network device",
            "Network connection failed",
            "Connectivity lost to remote device",

            # Database
            "Database service unavailable",
            "Database instance stopped",
            "Unable to connect to database service",
            "Database process is not responding",
        ],

        "Category": [
            "CPU Utilization",
            "CPU Utilization",
            "CPU Utilization",
            "CPU Utilization",

            "Disk Capacity",
            "Disk Capacity",
            "Disk Capacity",
            "Disk Capacity",

            "Connectivity",
            "Connectivity",
            "Connectivity",
            "Connectivity",

            "Database Availability",
            "Database Availability",
            "Database Availability",
            "Database Availability",
        ],
    }
)

    X, y = prepare_data(
        sample_data
    )

    X_train, X_test, y_train, y_test = (
        split_data(X, y)
    )

    (
        vectorizer,
        X_train_tfidf,
        X_test_tfidf,
    ) = vectorize_text(
        X_train,
        X_test,
    )

    results = evaluate_models(
        X_train_tfidf,
        X_test_tfidf,
        y_train,
        y_test,
    )

    print("Model Performance:\n")

    for name, result in results.items():

        print(
            f"{name}: "
            f"{result['accuracy']:.2%}"
        )

    (
        best_model_name,
        best_model,
    ) = select_best_model(
        results
    )

    print(
        f"\nBest Model: "
        f"{best_model_name}"
    )

    save_model(
        vectorizer,
        best_model,
    )
