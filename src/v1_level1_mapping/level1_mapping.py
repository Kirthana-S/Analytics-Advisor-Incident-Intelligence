"""
Analytics 2.0 - Version 1
Level 1 Incident Categorization

Purpose:
Automatically classify incident descriptions into high-level categories
using keyword and regular-expression based matching.

Note:
The original solution was developed using enterprise incident data.
All source paths, account information, and organizational identifiers
have been removed from this public version.
"""

import pandas as pd
import numpy as np


def categorize_level1(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign a Level 1 category based on patterns found in the
    incident Description field.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset containing a 'Description' column.

    Returns
    -------
    pandas.DataFrame
        Dataset with an additional 'Level_1_Category' column.
    """

    data = df.copy()

    # Create an empty Level 1 category column
    data["Level_1_Category"] = np.nan

    # Pattern matching is performed sequentially.
    # Once a record is categorized, later rules do not overwrite it.

    data.loc[
        data["Description"].str.match(r".*SAP.*", case=False, na=False),
        "Level_1_Category",
    ] = "SAP"

    data.loc[
        data["Description"].str.match(
            r".*System.*possibly.*", case=False, na=False
        )
        & data["Level_1_Category"].isna(),
        "Level_1_Category",
    ] = "System_Down"

    data.loc[
        data["Description"].str.match(
            r".*PerfMon.*", case=False, na=False
        )
        & data["Level_1_Category"].isna(),
        "Level_1_Category",
    ] = "Performance_Monitoring"

    data.loc[
        data["Description"].str.match(
            r".*(?:DISK SPACE|diskspace).*",
            case=False,
            na=False,
        )
        & data["Level_1_Category"].isna(),
        "Level_1_Category",
    ] = "Diskspace"

    data.loc[
        data["Description"].str.match(
            r".*NNMI.*", case=False, na=False
        )
        & data["Level_1_Category"].isna(),
        "Level_1_Category",
    ] = "Network_Monitoring"

    data.loc[
        data["Description"].str.match(
            r".*UXMON.*", case=False, na=False
        )
        & data["Level_1_Category"].isna(),
        "Level_1_Category",
    ] = "User_Experience_Monitoring"

    data.loc[
        data["Description"].str.match(
            r".*Test.*", case=False, na=False
        )
        & data["Level_1_Category"].isna(),
        "Level_1_Category",
    ] = "Test"

    data.loc[
        data["Description"].str.match(
            r".*Alert.*", case=False, na=False
        )
        & data["Level_1_Category"].isna(),
        "Level_1_Category",
    ] = "Alert"

    data.loc[
        data["Description"].str.match(
            r".*Agent.*", case=False, na=False
        )
        & data["Level_1_Category"].isna(),
        "Level_1_Category",
    ] = "Agent"

    data.loc[
        data["Description"].str.match(
            r".*Automatic service.*", case=False, na=False
        )
        & data["Level_1_Category"].isna(),
        "Level_1_Category",
    ] = "Windows_Service"

    data.loc[
        data["Description"].str.match(
            r".*Password.*Reset.*", case=False, na=False
        )
        & data["Level_1_Category"].isna(),
        "Level_1_Category",
    ] = "Password_Reset"

    data.loc[
        data["Description"].str.match(
            r".*Device.*", case=False, na=False
        )
        & data["Level_1_Category"].isna(),
        "Level_1_Category",
    ] = "Device"

    data.loc[
        data["Description"].str.match(
            r".*DBSPI.*", case=False, na=False
        )
        & data["Level_1_Category"].isna(),
        "Level_1_Category",
    ] = "Database_Monitoring"

    data.loc[
        data["Description"].str.match(
            r".*job.*", case=False, na=False
        )
        & data["Level_1_Category"].isna(),
        "Level_1_Category",
    ] = "Job_Monitoring"

    # Anything unmatched is grouped under Others
    data["Level_1_Category"] = data["Level_1_Category"].fillna("Others")

    return data


if __name__ == "__main__":

    # Public demonstration dataset.
    # Production data is intentionally not included in this repository.

    sample_incidents = pd.DataFrame(
        {
            "Incident_ID": [
                "INC001",
                "INC002",
                "INC003",
                "INC004",
                "INC005",
            ],
            "Description": [
                "CPU PerfMon threshold exceeded on server",
                "Password Reset requested for user",
                "Free disk space below threshold",
                "System possibly unavailable",
                "Unclassified application issue",
            ],
        }
    )

    categorized_data = categorize_level1(sample_incidents)

    print(categorized_data)
