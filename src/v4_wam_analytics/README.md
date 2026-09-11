# V4 – Whack-a-Mole (WAM) Analytics

## Objective

Version 4 introduced trend-based analytics to identify repetitive operational issues.

The goal was not only to categorize incidents, but also to determine whether recurring issues were:

- Increasing
- Persisting
- Decreasing
- Resolved

## Core Idea

Incidents were grouped using:

`Configuration Item + Level 2 Category`

This allowed the solution to identify repeated occurrences of the same issue against the same technical component.

## 30-Day Trend Window

WAM used a 30-day observation window.

The period was divided into:

```text
First 20 Days
     vs
Last 10 Days
```

## Processing Flow

Categorized Incident Data
        ↓
Configuration Item + Level 2
        ↓
Daily Incident Counts
        ↓
30-Day Trend Window
        ↓
First 20-Day Average
        vs
Last 10-Day Average
        ↓
Magnitude of Change
        ↓
Trend Classification
