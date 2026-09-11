"""
Analytics 2.0 - Version 2
Hierarchical Level 1 and Level 2 Incident Categorization

Major improvements from V1:
1. Introduced Level 2 sub-category classification.
2. Moved classification rules outside the Python code.
3. Automated rule execution using iterative processing.
4. Added tqdm progress tracking for large datasets.

All organizational data, internal paths and production classification
rules have been removed from this public implementation.
"""

import pandas as pd
import numpy as np
from tqdm import tqdm


def clean_incident_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic preprocessing required before classification.
    """

    data = df.copy()

    # Remove duplicate incidents
    if "Incident_ID" in data.columns:
        data = data.drop_duplicates(subset="Incident_ID")

    # Normalize multiline descriptions
    data["Description"] = (
        data["Description"]
        .fillna("")
        .replace(r"\n", " ", regex=True)
    )

    return data


def apply_level1_mapping(
    incidents: pd.DataFrame,
    level1_rules: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply Level 1 classification rules.

    Expected configuration columns:
        Level1
        L1_Regex
        L1_Priority
    """

    data = incidents.copy()

    data["Level1"] = np.nan
    data["L1_Regex"] = np.nan
    data["L1_Priority"] = np.nan

    for row in tqdm(
        range(len(level1_rules)),
        desc="Applying Level 1 rules",
    ):

        regex_pattern = level1_rules.loc[row, "L1_Regex"]
        category = level1_rules.loc[row, "Level1"]
        priority = level1_rules.loc[row, "L1_Priority"]

        match_condition = (
            data["Level1"].isna()
            & data["Description"].str.match(
                regex_pattern,
                case=False,
                na=False,
            )
        )

        data.loc[
            match_condition,
            ["Level1", "L1_Regex", "L1_Priority"],
        ] = [category, regex_pattern, priority]

    return data


def apply_level2_mapping(
    incidents: pd.DataFrame,
    level2_rules: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply Level 2 classification within the assigned Level 1 category.

    Expected configuration columns:
        Level1
        Level2
        L2_Regex
        L2_Priority
    """

    data = incidents.copy()

    data["Level2"] = np.nan
    data["L2_Regex"] = np.nan
    data["L2_Priority"] = np.nan

    for row in tqdm(
        range(len(level2_rules)),
        desc="Applying Level 2 rules",
    ):

        parent_category = level2_rules.loc[row, "Level1"]
        regex_pattern = level2_rules.loc[row, "L2_Regex"]
        sub_category = level2_rules.loc[row, "Level2"]
        priority = level2_rules.loc[row, "L2_Priority"]

        match_condition = (
            (data["Level1"] == parent_category)
            & data["Level2"].isna()
            & data["Description"].str.match(
                regex_pattern,
                case=False,
                na=False,
            )
        )

        data.loc[
            match_condition,
            ["Level2", "L2_Regex", "L2_Priority"],
        ] = [sub_category, regex_pattern, priority]

    return data


def classification_summary(
    df: pd.DataFrame,
    category_column: str,
) -> None:
    """
    Display classification coverage.
    """

    total = len(df)
    classified = df[category_column].notna().sum()
    unclassified = df[category_column].isna().sum()

    percentage = (
        classified / total * 100
        if total
        else 0
    )

    print(f"Total records: {total}")
    print(f"Classified: {classified}")
    print(f"Unclassified: {unclassified}")
    print(f"Classification coverage: {percentage:.2f}%")


if __name__ == "__main__":

    # Synthetic demonstration data only.
    incidents = pd.DataFrame(
        {
            "Incident_ID": [
                "INC001",
                "INC002",
                "INC003",
                "INC004",
            ],
            "Description": [
                "CPU utilization threshold exceeded",
                "Disk space threshold exceeded",
                "Network connectivity unavailable",
                "Database service unavailable",
            ],
        }
    )

    # Sanitized example configuration.
    level1_rules = pd.DataFrame(
        {
            "Level1": [
                "Compute",
                "Storage",
                "Network",
                "Database",
            ],
            "L1_Regex": [
                r".*CPU.*",
                r".*Disk.*",
                r".*Network.*",
                r".*Database.*",
            ],
            "L1_Priority": [1, 1, 1, 1],
        }
    )

    level2_rules = pd.DataFrame(
        {
            "Level1": [
                "Compute",
                "Storage",
                "Network",
                "Database",
            ],
            "Level2": [
                "CPU Utilization",
                "Disk Capacity",
                "Connectivity",
                "Service Availability",
            ],
            "L2_Regex": [
                r".*CPU.*utilization.*",
                r".*Disk.*space.*",
                r".*connectivity.*",
                r".*service.*unavailable.*",
            ],
            "L2_Priority": [1, 1, 1, 1],
        }
    )

    incidents = clean_incident_data(incidents)

    incidents = apply_level1_mapping(
        incidents,
        level1_rules,
    )

    incidents = apply_level2_mapping(
        incidents,
        level2_rules,
    )

    classification_summary(incidents, "Level1")
    classification_summary(incidents, "Level2")

    print("\nCategorized incidents:")
    print(
        incidents[
            [
                "Incident_ID",
                "Description",
                "Level1",
                "Level2",
            ]
        ]
    )
