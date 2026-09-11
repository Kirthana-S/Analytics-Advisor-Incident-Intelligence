"""
Analytics 2.0 - Version 4
Whack-a-Mole (WAM) Analytics

Purpose:
Identify repetitive incident patterns and determine whether issue
volumes are increasing, stable, decreasing, or resolved over time.

All organizational identifiers and production data have been removed.
"""

import pandas as pd
import numpy as np


def prepare_daily_trend(
    incidents: pd.DataFrame,
    date_column: str = "Created_Date",
) -> pd.DataFrame:
    """
    Aggregate incidents by CI, Level 2 category and day.
    """

    data = incidents.copy()

    data[date_column] = pd.to_datetime(
        data[date_column],
        errors="coerce",
    )

    data = data.dropna(subset=[date_column])

    daily_trend = (
        data.groupby(
            [
                "Configuration_Item",
                "Level2",
                data[date_column].dt.date,
            ]
        )
        .size()
        .reset_index(name="Incident_Count")
    )

    daily_trend = daily_trend.rename(
        columns={date_column: "Incident_Date"}
    )

    return daily_trend


def calculate_wam_metrics(
    daily_trend: pd.DataFrame,
    reference_date=None,
) -> pd.DataFrame:
    """
    Compare the first 20 days and last 10 days of a 30-day window.

    Returns one row per CI + Level2 combination with:
    - earlier average
    - recent average
    - magnitude of change
    - trend status
    """

    data = daily_trend.copy()

    data["Incident_Date"] = pd.to_datetime(
        data["Incident_Date"]
    )

    if reference_date is None:
        reference_date = data["Incident_Date"].max()

    reference_date = pd.to_datetime(reference_date)

    window_start = reference_date - pd.Timedelta(days=29)
    recent_start = reference_date - pd.Timedelta(days=9)

    window_data = data[
        (data["Incident_Date"] >= window_start)
        & (data["Incident_Date"] <= reference_date)
    ].copy()

    results = []

    for (ci, level2), group in window_data.groupby(
        ["Configuration_Item", "Level2"]
    ):

        earlier_period = group[
            group["Incident_Date"] < recent_start
        ]

        recent_period = group[
            group["Incident_Date"] >= recent_start
        ]

        earlier_avg = (
            earlier_period["Incident_Count"].sum() / 20
        )

        recent_avg = (
            recent_period["Incident_Count"].sum() / 10
        )

        if earlier_avg == 0:
            magnitude = np.inf if recent_avg > 0 else 0
        else:
            magnitude = (
                recent_avg - earlier_avg
            ) / earlier_avg

        status = classify_issue_status(
            earlier_avg,
            recent_avg,
        )

        results.append(
            {
                "Configuration_Item": ci,
                "Level2": level2,
                "Earlier_Average": round(earlier_avg, 2),
                "Recent_Average": round(recent_avg, 2),
                "Magnitude": magnitude,
                "Trend_Status": status,
            }
        )

    return pd.DataFrame(results)


def classify_issue_status(
    earlier_avg: float,
    recent_avg: float,
) -> str:
    """
    Classify the trend of an issue.

    Thresholds below are simplified for the public demonstration.
    """

    if earlier_avg > 0 and recent_avg == 0:
        return "Issue Solved"

    if recent_avg > earlier_avg:
        return "Issue Increased"

    if 0 < recent_avg < earlier_avg:
        return "Issue Decreasing"

    if recent_avg == earlier_avg and recent_avg > 0:
        return "Issue Existing"

    return "No Significant Activity"


if __name__ == "__main__":

    # Synthetic demonstration dataset
    sample_data = pd.DataFrame(
        {
            "Incident_ID": [
                "INC001",
                "INC002",
                "INC003",
                "INC004",
                "INC005",
                "INC006",
            ],
            "Configuration_Item": [
                "SERVER_A",
                "SERVER_A",
                "SERVER_A",
                "SERVER_B",
                "SERVER_B",
                "SERVER_B",
            ],
            "Level2": [
                "CPU Utilization",
                "CPU Utilization",
                "CPU Utilization",
                "Disk Capacity",
                "Disk Capacity",
                "Disk Capacity",
            ],
            "Created_Date": [
                "2026-01-01",
                "2026-01-15",
                "2026-01-28",
                "2026-01-03",
                "2026-01-08",
                "2026-01-12",
            ],
        }
    )

    daily_trend = prepare_daily_trend(sample_data)

    wam_results = calculate_wam_metrics(
        daily_trend,
        reference_date="2026-01-30",
    )

    print(wam_results)
