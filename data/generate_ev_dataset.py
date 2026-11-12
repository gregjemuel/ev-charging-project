"""
generate_ev_dataset.py
----------------------
Creates a SYNTHETIC electric-vehicle charging-session dataset (Kenya-style) for
DSA 1080A Future Data Lab, Project 02: Electric Mobility and Charging Patterns.

IMPORTANT: every row is simulated. No real drivers, vehicles or stations are
represented. Patterns in this data are the result of the assumptions written
below, NOT real-world evidence. Say so in your report.

Run:   python generate_ev_dataset.py
Needs: pandas, numpy
Output (in the same folder):
    ev_charging_sessions_raw.csv    -> mildly messy version for Weeks 2-3 (cleaning practice)
    ev_charging_sessions_clean.csv  -> tidy reference version
"""

import numpy as np
import pandas as pd

SEED = 2026
N_SESSIONS = 18_000            # unique sessions (minimum required is 15,000)
START_DATE = "2026-01-01"
END_DATE = "2026-06-30"
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- stations
CITY_AREAS = {
    "Nairobi": ["Westlands", "Kilimani", "Karen", "Eastleigh", "Upper Hill", "Thika Road",
                "Embakasi", "Lavington", "Gigiri", "CBD", "Ngong Road", "Syokimau"],
    "Mombasa": ["Nyali", "Bamburi", "Mombasa CBD", "Likoni"],
    "Kisumu": ["Milimani", "Kisumu CBD", "Mamboleo"],
    "Nakuru": ["Nakuru CBD", "Naivasha Road", "Lanet"],
    "Eldoret": ["Eldoret CBD", "Elgon View", "Kapsoya"],
}
CITY_STATIONS = {"Nairobi": 28, "Mombasa": 7, "Kisumu": 4, "Nakuru": 5, "Eldoret": 4}
STATION_TYPES = ["Shopping Mall", "Fuel Station", "Office Park",
                 "Residential Estate", "Highway Stop", "Transport Hub"]

stations = []
sid = 1
for city, n in CITY_STATIONS.items():
    for _ in range(n):
        stype = rng.choice(STATION_TYPES, p=[.24, .22, .18, .16, .12, .08])
        if city in ("Nakuru", "Eldoret") and rng.random() < .5:
            stype = "Highway Stop"
        has_dc = (stype in ("Fuel Station", "Highway Stop", "Transport Hub")) or rng.random() < .35
        dc_options = {"CCS2": float(rng.choice([50, 60]))}
        if has_dc and rng.random() < .45:
            dc_options["CHAdeMO"] = 50.0
        if has_dc and rng.random() < .25:
            dc_options["GB/T"] = 30.0
        conns = {"Type 2": float(rng.choice([7.4, 22.0], p=[.6, .4]))}
        if has_dc:
            conns.update(dc_options)
        stations.append({
            "station_id": f"STN-{sid:03d}",
            "city": city,
            "location": f"{city} - {rng.choice(CITY_AREAS[city])}",
            "station_type": stype,
            "connectors": conns,
            "has_dc": has_dc,
            "ac_rate": rng.uniform(28, 38),        # KES per kWh
            "dc_rate": rng.uniform(46, 60),
            "popularity": rng.lognormal(0, .55) * (2.0 if city == "Nairobi" else 1.0),
        })
        sid += 1

# ---------------------------------------------------------------- vehicles
# (typical kWh per session mean, sd-ish, max AC kW accepted, max DC kW accepted)
VEHICLES = {
    "Electric Motorbike": dict(e_mean=2.6, e_sd=.8, ac=3.3, dc=0.0),
    "Electric Car": dict(e_mean=22, e_sd=10, ac=7.4, dc=60.0),
    "Electric Van": dict(e_mean=32, e_sd=13, ac=11.0, dc=50.0),
    "Electric Bus": dict(e_mean=85, e_sd=25, ac=0.0, dc=120.0),
}
VEHICLE_MIX = {  # probabilities per station type [Motorbike, Car, Van, Bus]
    "Shopping Mall": [.10, .80, .09, .01],
    "Fuel Station": [.08, .62, .26, .04],
    "Office Park": [.12, .78, .09, .01],
    "Residential Estate": [.18, .78, .04, .00],
    "Highway Stop": [.04, .58, .28, .10],
    "Transport Hub": [.10, .30, .25, .35],
}
VEH_NAMES = list(VEHICLES)

# ---------------------------------------------------------------- time patterns
def hour_profile(peaks, base=.15):
    w = np.full(24, base)
    for h, amp in peaks.items():
        for d in range(-2, 3):
            w[(h + d) % 24] += amp * np.exp(-(d ** 2) / 2.0)
    return w / w.sum()

HOUR_W = {
    "Office Park": hour_profile({8: 1.0, 13: .6, 17: .3}),
    "Shopping Mall": hour_profile({12: .6, 15: .7, 19: .8}),
    "Residential Estate": hour_profile({6: .4, 19: 1.0, 22: .7}),
    "Highway Stop": hour_profile({9: .7, 13: .6, 17: .6}, base=.3),
    "Fuel Station": hour_profile({8: .7, 13: .5, 18: .8}, base=.25),
    "Transport Hub": hour_profile({6: .7, 12: .4, 20: .6}, base=.35),
}

HOLIDAYS = pd.to_datetime(["2026-01-01", "2026-03-20", "2026-04-03",
                           "2026-04-06", "2026-05-01", "2026-06-01"])
days = pd.date_range(START_DATE, END_DATE, freq="D")
def day_type(d):
    if d in HOLIDAYS:
        return "Public Holiday"
    return "Weekend" if d.dayofweek >= 5 else "Weekday"

day_types = np.array([day_type(d) for d in days])
growth = np.linspace(1.0, 1.6, len(days))            # EV adoption grows over time
dow_factor = np.where(day_types == "Weekday", 1.0,
                      np.where(day_types == "Weekend", .82, .70))
day_w = growth * dow_factor * rng.normal(1, .06, len(days)).clip(.8, 1.2)
day_w /= day_w.sum()

# ---------------------------------------------------------------- sessions
st_w = np.array([s["popularity"] for s in stations]); st_w /= st_w.sum()
rows = []
day_idx = rng.choice(len(days), size=N_SESSIONS, p=day_w)
st_idx = rng.choice(len(stations), size=N_SESSIONS, p=st_w)

for di, si in zip(day_idx, st_idx):
    s = stations[si]
    p = np.array(VEHICLE_MIX[s["station_type"]], dtype=float)
    if not s["has_dc"]:
        p[3] = 0.0                                    # buses need DC
        p[2] *= .5
    p /= p.sum()
    veh = rng.choice(VEH_NAMES, p=p)
    v = VEHICLES[veh]

    # connector choice
    avail = s["connectors"]
    if veh == "Electric Motorbike":
        conn = "Type 2"
    elif veh == "Electric Bus":
        opts = [c for c in avail if c != "Type 2"]
        conn = rng.choice(opts)
    else:
        dc_opts = [c for c in avail if c != "Type 2"]
        if dc_opts and rng.random() < (.35 if s["station_type"] in ("Residential Estate", "Office Park") else .6):
            conn = rng.choice(dc_opts)
        else:
            conn = "Type 2"
    is_dc = conn != "Type 2"
    station_kw = avail[conn]
    vehicle_kw = v["dc"] if is_dc else v["ac"]
    if vehicle_kw == 0:                                # e.g. car-only AC logic safety
        conn, is_dc = "Type 2", False
        station_kw, vehicle_kw = avail["Type 2"], v["ac"] or 7.4

    # energy delivered (kWh)
    mu = np.log(v["e_mean"] ** 2 / np.sqrt(v["e_sd"] ** 2 + v["e_mean"] ** 2))
    sg = np.sqrt(np.log(1 + (v["e_sd"] / v["e_mean"]) ** 2))
    energy = float(np.clip(rng.lognormal(mu, sg), .8, v["e_mean"] * 3.2))
    if is_dc:
        energy *= rng.uniform(.9, 1.15)               # fast chargers: top-ups of larger size

    # duration (minutes)
    eff_kw = min(station_kw, vehicle_kw) * rng.uniform(.65, .92)
    minutes = energy / eff_kw * 60 + rng.uniform(2, 6)
    if s["station_type"] == "Residential Estate" and not is_dc and rng.random() < .5:
        minutes += rng.exponential(120)               # car left plugged in
    if s["station_type"] == "Office Park" and not is_dc and rng.random() < .4:
        minutes += rng.exponential(60)
    minutes = int(round(min(minutes, 720)))

    # start time
    hour = int(rng.choice(24, p=HOUR_W[s["station_type"]]))
    start = days[di] + pd.Timedelta(hours=hour, minutes=int(rng.integers(0, 60)),
                                    seconds=int(rng.integers(0, 60)))
    end = start + pd.Timedelta(minutes=minutes)

    # cost (KES, VAT included): per-kWh tariff, +10% evening peak (18:00-21:59)
    rate = s["dc_rate"] if is_dc else s["ac_rate"]
    peak = 1.10 if 18 <= start.hour <= 21 else 1.0
    cost = round(energy * rate * peak, 2)

    # payment
    pm_p = {"Electric Motorbike": [.82, .03, .15, .00],
            "Electric Car": [.55, .20, .22, .03],
            "Electric Van": [.30, .12, .13, .45],
            "Electric Bus": [.05, .00, .05, .90]}[veh]
    pay = rng.choice(["M-Pesa", "Card", "App Wallet", "Corporate Account"], p=pm_p)

    rows.append(dict(
        start_time=start, end_time=end, station_id=s["station_id"], city=s["city"],
        location=s["location"], station_type=s["station_type"], vehicle_type=veh,
        connector_type=conn, energy_kwh=round(energy, 2), duration_min=minutes,
        cost_kes=cost, day_type=day_types[di], payment_method=pay))

clean = pd.DataFrame(rows).sort_values("start_time").reset_index(drop=True)
clean.insert(0, "session_id", [f"EVS-{i:06d}" for i in range(1, len(clean) + 1)])
clean["start_time"] = clean["start_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
clean["end_time"] = clean["end_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
clean.to_csv("ev_charging_sessions_clean.csv", index=False)

# ---------------------------------------------------------------- make the RAW (messy) version
# Small, realistic problems so Week 2 (audit) and Week 3 (cleaning) have real work to do.
raw = clean.copy()
n = len(raw)
def pick(k): return rng.choice(n, size=k, replace=False)

for col, frac in [("payment_method", .02), ("connector_type", .012),
                  ("cost_kes", .015), ("duration_min", .01), ("location", .008)]:
    raw.loc[pick(int(n * frac)), col] = np.nan

# inconsistent category text (case / spaces)
idx = pick(int(n * .02)); raw.loc[idx, "station_type"] = raw.loc[idx, "station_type"].str.upper()
idx = pick(int(n * .015)); raw.loc[idx, "vehicle_type"] = raw.loc[idx, "vehicle_type"].str.lower()
idx = pick(int(n * .01)); raw.loc[idx, "city"] = " " + raw.loc[idx, "city"] + " "

# a few extreme / invalid values (typing slips)
idx = pick(12); raw.loc[idx, "energy_kwh"] = (raw.loc[idx, "energy_kwh"] * 10).round(2)
idx = pick(6);  raw.loc[idx, "energy_kwh"] = -raw.loc[idx, "energy_kwh"]
idx = pick(5);  raw.loc[idx, "cost_kes"] = 0

# exact duplicate rows (system re-sent records)
dups = raw.sample(90, random_state=SEED)
raw = pd.concat([raw, dups]).sample(frac=1, random_state=SEED).sort_values("session_id", kind="stable")
raw.to_csv("ev_charging_sessions_raw.csv", index=False)

print("clean:", clean.shape, "| raw:", raw.shape)
