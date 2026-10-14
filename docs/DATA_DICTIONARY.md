# Data Dictionary

## Scope and status conventions

This dictionary describes `data/Crop_Yield_original.csv`. Metadata statuses mean:

- **CONFIRMED** — supported by the source file, deterministic Phase 1 validation, or metadata explicitly approved by the human analyst.
- **INFERRED** — a reasonable interpretation that is not supported by documentary evidence.
- **UNKNOWN** — not documented and not safely inferable.

Ranges below are **observed dataset ranges**, calculated during validation. They are not scientifically valid limits, recommended ranges, or evidence that the values represent real observations. Categorical domains are observed values, not necessarily exhaustive real-world domains.

| Variable | Data type | Description | Unit | Categorical domain | Observed range | Source of definition | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| `N` | Integer | Recorded nitrogen input or concentration | kg | Not applicable | 30–179 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Whether this is a total, concentration, or application rate is UNKNOWN. |
| `P` | Integer | Recorded phosphorus input or concentration | kg | Not applicable | 15–99 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Whether this is a total, concentration, or application rate is UNKNOWN. |
| `K` | Integer | Recorded potassium input or concentration | kg | Not applicable | 20–149 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Whether this is a total, concentration, or application rate is UNKNOWN. |
| `Soil_pH` | Float | Soil acidity/alkalinity measurement | pH scale | Not applicable | 4.80–8.20 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Measurement method is UNKNOWN. |
| `Soil_Moisture` | Float | Soil moisture level | % | Not applicable | 15.00–64.99 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Measurement method and moisture basis are UNKNOWN. |
| `Soil_Type` | Categorical | Soil classification used by the dataset | Not applicable | Clay; Loamy; Sandy; Silt | Not applicable | Human-approved metadata; source values | CONFIRMED | Dataset classification is described without assuming scientific sampling. |
| `Organic_Carbon` | Float | Soil organic-carbon measurement | ppm | Not applicable | 0.30–1.60 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Measurement method is UNKNOWN. |
| `Temperature` | Float | Recorded environmental temperature | °C | Not applicable | 10.00–40.00 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Aggregation period and measurement method are UNKNOWN. |
| `Humidity` | Float | Recorded relative humidity | % | Not applicable | 30.01–89.99 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Aggregation period and measurement method are UNKNOWN. |
| `Rainfall` | Float | Recorded rainfall quantity | mm | Not applicable | 300.70–2799.26 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Accumulation period is UNKNOWN. |
| `Sunlight_Hours` | Float | Recorded average duration of sunlight | Average hours/day | Not applicable | 4.00–11.00 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Averaging period is UNKNOWN. |
| `Wind_Speed` | Float | Recorded average wind speed | km/hour | Not applicable | 1.00–18.00 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Averaging period and measurement method are UNKNOWN. |
| `Region` | Categorical | Geographic-region label used by the dataset | Not applicable | Central; East; North; South; West | Not applicable | Human-approved metadata; source values | CONFIRMED | Actual geography represented by the labels is UNKNOWN. |
| `Altitude` | Integer | Elevation associated with the observation | metres | Not applicable | 0–2199 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Vertical datum and measurement method are UNKNOWN. |
| `Crop_Type` | Categorical | Crop assigned to the observation | Not applicable | Cotton; Maize; Potato; Rice; Sugarcane; Wheat | Not applicable | Human-approved metadata; source values | CONFIRMED | Observed dataset categories only. |
| `Irrigation_Type` | Categorical | Irrigation classification | Not applicable | Canal; Drip; Rainfed; Sprinkler | Not applicable | Human-approved metadata; source values | CONFIRMED | Classification method is UNKNOWN. |
| `Fertilizer_Used` | Float | Recorded fertiliser-use quantity | kg/ha | Not applicable | 60.00–349.96 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Product composition and application period are UNKNOWN. |
| `Pesticide_Used` | Float | Recorded pesticide-use quantity | litres/ha | Not applicable | 0.00–25.00 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Product composition and application period are UNKNOWN. |
| `Crop_Yield_ton_per_hectare` | Float | Crop-yield outcome recorded by the dataset | tonnes/ha | Not applicable | 1.76–80.99 | Human-approved metadata; Phase 1 manifest | CONFIRMED | Measurement period and method are UNKNOWN. This is the intended future modelling target, but no modelling is authorised yet. |

## Dataset-level metadata not established

The dataset's observed, synthetic, simulated, augmented, or other generation status is **UNKNOWN**. Collection design, sampling method, sampling frame, dates, geographic coverage, source organisation, Kaggle record, and transformation history before receipt are also **UNKNOWN**.

