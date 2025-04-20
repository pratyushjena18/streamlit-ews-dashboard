
import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="EWS Risk Scoring Dashboard", layout="wide")

# Title
st.title("📊 Early Warning System (EWS) Dashboard for MSME & Co-Lending")

# Sample borrower data
data = {
    "Borrower ID": ["MSME_1023", "MSME_2045", "POOL_3401", "COLO_8762"],
    "GST Decline (%)": [37.5, 15.0, 60.0, 25.0],
    "EMI Default Rate (%)": [25.0, 0.0, 50.0, 0.0],
    "NBFC Partner Health": [0.7, 0.85, 0.6, 0.9],
    "Geo Risk (1=Yes)": [1, 0, 1, 0],
    "Cash Flow Stress (%)": [63.6, 20.0, 80.0, 10.0],
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Weights for scoring
weights = {
    "gst_decline": 0.25,
    "emi_consistency": 0.25,
    "nbfc_partner_health": 0.2,
    "geo_risk": 0.15,
    "cash_flow_stress": 0.15
}

# Scoring function
def score_row(row):
    gst_score = row["GST Decline (%)"]
    emi_score = row["EMI Default Rate (%)"]
    nbfc_score = (1 - row["NBFC Partner Health"]) * 100
    geo_score = 100 if row["Geo Risk (1=Yes)"] == 1 else 0
    cash_score = row["Cash Flow Stress (%)"]

    final_score = (weights["gst_decline"] * gst_score +
                   weights["emi_consistency"] * emi_score +
                   weights["nbfc_partner_health"] * nbfc_score +
                   weights["geo_risk"] * geo_score +
                   weights["cash_flow_stress"] * cash_score)

    if final_score < 30:
        category = "🟢 Low"
    elif final_score < 60:
        category = "🟡 Medium"
    else:
        category = "🔴 High"

    return round(final_score, 2), category

# Apply scoring
df[["Risk Score", "Risk Category"]] = df.apply(score_row, axis=1, result_type="expand")

# Display the full DataFrame with conditional coloring
st.dataframe(df.style
    .applymap(lambda v: 'background-color: #ffcccc' if isinstance(v, str) and 'High' in v else '', subset=['Risk Category'])
    .applymap(lambda v: 'background-color: #ffffcc' if isinstance(v, str) and 'Medium' in v else '', subset=['Risk Category'])
    .applymap(lambda v: 'background-color: #ccffcc' if isinstance(v, str) and 'Low' in v else '', subset=['Risk Category'])
)

# Bar chart for visual
st.subheader("📈 Risk Score Distribution")
st.bar_chart(df.set_index("Borrower ID")["Risk Score"])
