import json
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

print("Loading Longitudinal EHR Cohort Tracker...")

# 1. Ingest JSON data matrix into a structured DataFrame
with open("ehr_patient_cohort.json", "r") as file:
    data = json.load(file)
df = pd.DataFrame(data)

# 2. Initialize Kaplan-Meier Fitters for both clinical strata
kmf_exposed = KaplanMeierFitter()
kmf_reference = KaplanMeierFitter()

# Split the cohorts based on social determinants of health (SDoH) risk vectors
exposed_cohort = df[df["cohort_strata"] == "Exposed_SDoH"]
reference_cohort = df[df["cohort_strata"] == "Reference_Group"]

plt.figure(figsize=(9, 5))

# 3. Fit data: 'durations' is time-to-event, 'event_observed' flags true diagnosis vs right-censoring
kmf_exposed.fit(
    durations=exposed_cohort["observation_days"], 
    event_observed=exposed_cohort["ptsd_diagnosed"], 
    label="High SDoH Vulnerability Matrix"
)
kmf_exposed.plot_survival_function(ci_show=False, color="crimson", linewidth=2.5, marker="o")

kmf_reference.fit(
    durations=reference_cohort["observation_days"], 
    event_observed=reference_cohort["ptsd_diagnosed"], 
    label="Socioeconomic Reference Group"
)
kmf_reference.plot_survival_function(ci_show=False, color="navy", linewidth=2.5, marker="x")

# 4. Standardize Academic/Clinical Graph Formatting
plt.title("Time-to-Diagnosis Probability Matrix for PTSD via Longitudinal EHR Data", fontsize=13, pad=15)
plt.xlabel("Timeline Ingestion Window (Days Post-Trauma Event Entry)", fontsize=11)
plt.ylabel("Probability of Remaining PTSD-Free (Survival Rate)", fontsize=11)
plt.ylim(0, 1.05)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# 5. Save the real analytical visualization image asset
plt.savefig("ptsd_survival_curve.png", dpi=300)
print("Success! Kaplan-Meier survival curves generated as 'ptsd_survival_curve.png'")
