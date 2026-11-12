# Data Dictionary: EV Charging Sessions (SYNTHETIC)

**Dataset:** `ev_charging_sessions_raw.csv` (18,090 rows) and `ev_charging_sessions_clean.csv` (18,000 rows)
**Columns:** 14 | **Period:** 1 Jan 2026 to 30 Jun 2026 | **Currency:** Kenya shillings (KES)
**Nature of data:** simulated for teaching. Not real-world evidence.

| # | Column | Type | Meaning | Units / allowed values | Missing expected? |
|---|--------|------|---------|------------------------|-------------------|
| 1 | session_id | text | Unique ID of one charging session | `EVS-000001` ... | No |
| 2 | start_time | datetime | When charging began | `YYYY-MM-DD HH:MM:SS` | No |
| 3 | end_time | datetime | When the vehicle was unplugged | `YYYY-MM-DD HH:MM:SS` | No |
| 4 | station_id | text | Charging station ID (48 stations) | `STN-001` ... `STN-048` | No |
| 5 | city | category | City of the station | Nairobi, Mombasa, Kisumu, Nakuru, Eldoret | No |
| 6 | location | text | City and area of the station | e.g. `Nairobi - Westlands` | Rare |
| 7 | station_type | category | Kind of site hosting the charger | Shopping Mall, Fuel Station, Office Park, Residential Estate, Highway Stop, Transport Hub | No |
| 8 | vehicle_type | category | Type of electric vehicle | Electric Motorbike, Electric Car, Electric Van, Electric Bus | No |
| 9 | connector_type | category | Plug used | Type 2 (AC), CCS2, CHAdeMO, GB/T (DC fast) | Rare |
| 10 | energy_kwh | number | Electricity delivered | kWh, should be > 0 | No |
| 11 | duration_min | integer | Plugged-in time | minutes, should be > 0 | Rare |
| 12 | cost_kes | number | Amount charged, VAT included | KES, should be > 0 | Rare |
| 13 | day_type | category | Kind of day | Weekday, Weekend, Public Holiday | No |
| 14 | payment_method | category | How the driver paid | M-Pesa, Card, App Wallet, Corporate Account | Rare |

## Notes
- `duration_min` is plugged-in time, not pure charging time. Residential and office sessions can be long because cars stay plugged in.
- The **raw** file contains small, realistic data-quality problems for Weeks 2 and 3 (missing values, duplicates, inconsistent text, a few suspicious numbers). Find them with your own audit and document each one. The **clean** file is a tidy reference.
- Public holidays used: 1 Jan, 20 Mar, 3 Apr, 6 Apr, 1 May, 1 Jun 2026 (approximate).
