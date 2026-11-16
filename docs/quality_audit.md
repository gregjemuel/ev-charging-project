# Data Quality Audit: ev_charging_sessions_raw.csv

| # | Check | Column(s) | Finding | Evidence |
|---|-------|-----------|---------|----------|
| 1 | Missing values | payment_method, cost_kes, connector_type, duration_min, location | 5 columns have empty cells; payment_method has the most (about 2%) | 02_exploration.ipynb, missing-values table |
| 2 | Duplicate rows | all columns | 90 exact duplicate rows | df.duplicated().sum() |
| 3 | Invalid numeric values | energy_kwh | 6 negative values | negative energy count |
| 4 | Suspicious values | cost_kes | 5 sessions with zero cost | zero cost count |
| 5 | Outliers | energy_kwh | some cars and vans have energy values far above their averages; flagged, not deleted | groupby energy summary by vehicle type |
| 6 | Inconsistent categories | vehicle_type, station_type, city | same category written in different ways (case and spaces) | value_counts output |
| 7 | Date parsing | start_time, end_time | [write what you found] | date parsing cell |

Source data was not changed. All fixes are planned for Week 3.