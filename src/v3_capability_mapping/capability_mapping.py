"""
Analytics 2.0 - Version 3
Capability-Level Incident Mapping

Purpose:
Map individual operational / assignment groups into broader
technical capabilities and enable capability-aware analysis.

This public version uses synthetic organizational mappings only.
Original enterprise team structures are excluded.
"""

import pandas as pd


def map_capabilities(
    incidents: pd.DataFrame,
    capability_mapping: pd.DataFrame,
) -> pd.DataFrame:
    """
    Map individual assignment groups to broader capabilities.

    Expected incident columns:
        Incident_ID
        Description
        Assignment_Group

    Expected mapping columns:
        Assignment_Group
        Capability
    """

    data = incidents.copy()

    mapped_data = data.merge(
        capability_mapping,
        how="left",
        on="Assignment_Group",
    )

    mapped_data["Capability"] = (
        mapped_data["Capability"]
        .fillna("Unmapped")
    )

    return mapped_data


def capability_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate incident counts by capability.
    """

    return (
        df.groupby("Capability")
        .size()
        .reset_index(name="Incident_Count")
        .sort_values(
            "Incident_Count",
            ascending=False,
        )
    )


if __name__ == "__main__":

    # Synthetic incident records
    incidents = pd.DataFrame(
        {
            "Incident_ID": [
                "INC001",
                "INC002",
                "INC003",
                "INC004",
                "INC005",
            ],
            "Description": [
                "Network connectivity unavailable",
                "Disk space threshold exceeded",
                "CPU utilization exceeded",
                "Database service unavailable",
                "Windows service stopped",
            ],
            "Assignment_Group": [
                "OPS-NETWORK-A",
                "OPS-STORAGE-A",
                "OPS-COMPUTE-A",
                "OPS-DATABASE-A",
                "OPS-WINDOWS-A",
            ],
        }
    )

    # Synthetic working-group-to-capability mapping
    capability_mapping = pd.DataFrame(
        {
            "Assignment_Group": [
                "OPS-NETWORK-A",
                "OPS-STORAGE-A",
                "OPS-COMPUTE-A",
                "OPS-DATABASE-A",
                "OPS-WINDOWS-A",
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

    mapped = map_capabilities(
        incidents,
        capability_mapping,
    )

    print("Mapped Incidents:\n")
    print(mapped)

    print("\nCapability Summary:\n")
    print(capability_summary(mapped))
