# V1 – Level 1 Incident Categorization

## Objective

Version 1 established the baseline incident categorization framework.

The objective was to automatically classify incident records into high-level categories by analyzing the text available in the `Description` field.

## Approach

V1 used predefined keywords and regular-expression patterns to identify common incident themes.

Examples included categories related to:

- System availability
- Performance monitoring
- Disk space
- Network monitoring
- User experience monitoring
- Alerts
- Agents
- Windows services
- Password resets
- Devices
- Database monitoring
- Job monitoring

## Processing Flow

```text
Incident Dataset
      ↓
Description
      ↓
Keyword / Regex Matching
      ↓
Level 1 Category
      ↓
Categorized Dataset
