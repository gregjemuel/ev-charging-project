# Project Proposal: EV Charging Patterns in Kenya

**Course:** DSA 1080A Programming for Data Science | **Project:** 02
**Group leader:** Greg Jemuel Muriuki (202609022)

## 1. Problem and purpose
Electric vehicles are growing in popularity, and charging stations need to be placed and priced well. This project investigates how EV charging sessions vary by city, station type, vehicle type, time of day and cost, so that we can make realistic recommendations.

## 2. Target users
- Charging network operators deciding where to add chargers
- City planners and utility companies planning electricity demand
- Drivers and fleet managers choosing when and where to charge

## 3. Objectives
**Overall objective:** To analyse EV charging sessions across five Kenyan cities to understand when and where charging demand is highest and how session length and cost vary.

**Specific objectives:**
1. Identify the stations, cities and times of day with the most charging sessions.
2. Compare session duration and energy use across vehicle types and station types.
3. Examine how charging cost relates to energy supplied and connector type.

## 4. Research questions
1. Which cities and station types have the most charging sessions?
2. At what hours and on which day types is charging busiest?
3. Which station types have the longest sessions?
4. How does cost change with the energy supplied (kWh)?
5. Which vehicle types use fast chargers most?

## 5. Dataset and source information
- **Name:** EV Charging Sessions (synthetic)
- **Type:** SYNTHETIC. Every row is simulated. It does not describe real drivers or stations.
- **Creator and source:** Generated with `generate_ev_dataset.py` (fixed random seed 2026) with help from an AI assistant (Claude by Anthropic).
- **Licence:** Created for this course project. Not published as open data.
- **Collection period:** 1 January to 30 June 2026 (simulated).
- **Size:** 18,090 rows and 14 columns (raw version, includes 90 duplicate rows to be cleaned in Week 3).
- **Approval:** [Lecturer approved synthetic data on: date]

## 6. Limitations
- All patterns come from the assumptions in the generator, so they are not real-world evidence and cannot be generalised.
- Tariffs, vehicle mix, time-of-day patterns and growth rates are assumed values.
- The raw file contains deliberately added data-quality problems that we will find and document in Weeks 2 and 3.

## 7. Team
See README.md for names, admission numbers and roles.