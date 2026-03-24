# Data Directory

This folder stores all datasets used in the forecasting pipeline.

- `raw/`: immutable source files as originally received.
- `external/`: third-party reference datasets (rates, benchmarks, macro indicators).
- `processed/`: cleaned and transformed datasets ready for modeling.
- `features/`: feature-engineered outputs used by training/inference.

Keep sensitive financial data out of version control.
