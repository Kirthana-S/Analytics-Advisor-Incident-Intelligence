"""
Analytics 2.0 - Version 3
Capability-Level Incident Mapping

Purpose:
Extend Level 1 and Level 2 incident classification by mapping
classified incidents to broader operational capability groups.

This public version uses synthetic mappings only.
All organizational names, internal teams, customer information,
and production mapping data have been removed.
"""

import pandas as pd


def map_capabilities(
    incidents: pd.DataFrame,
    capability_mapping: pd.DataFrame,
) -> pd.DataFrame:
    """
    Map classified incidents to broader capability groups.

    Expected incident columns:
        Incident_ID
        Level1
        Level2

    Expected mapping columns:
        Level1
        Level2
        Capability
    """

    data = incidents.copy()

    mapped_data = data.merge(
        capability_mapping,
        how="left",
        on=["Level1", "Level2"],
    )

    mapped_data["Capability"] = mapped_data["Capability"].fillna(
        "Unmapped"
    )

    return mapped_data


def capability_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a simple incident count summary by capability.
    """

    summary = (
        df.groupby("Capability")
        .size()
        .reset_index(name="Incident_Count")
        .sort_values(
            by="Incident_Count",
            ascending=False,
        )
    )

    return summary


if __name__ == "__main__":

    # Synthetic incident classification output from V2
    incidents = pd.DataFrame(
        {
            "Incident_ID": [
                "INC001",
                "INC002",
                "INC003",
                "INC004",
                "INC005",
            ],
            "Level1": [
                "Network",
                "Storage",
                "Compute",
                "Database",
                "Compute",
            ],
            "Level2": [
                "Connectivity",
                "Disk Capacity",
                "CPU Utilization",
                "Service Availability",
                "Windows Service",
            ],
        }
    )

    # Synthetic capability mapping
    capability_mapping = pd.DataFrame(
        {
            "Level1": [
                "Network",
                "Storage",
                "Compute",
                "Database",
                "Compute",
            ],
            "Level2": [
                "Connectivity",
                "Disk Capacity",
                "CPU Utilization",
                "Service Availability",
                "Windows Service",
            ],
            "Capability": [
                "Network",
                "Storage",
                "CloudOps",
                "Database",
                "Windows",
            ],
        }
    )

    mapped_incidents = map_capabilities(
        incidents,
        capability_mapping,
    )

    print("Mapped Incidents:\n")
    print(mapped_incidents)

    print("\nCapability Summary:\n")
    print(capability_summary(mapped_incidents))
