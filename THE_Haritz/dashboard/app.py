import streamlit as st
import time
import requests
import pandas as pd
import altair as alt
from datetime import datetime, timezone

# 1. Streamlit page config
st.set_page_config(page_title="Wallet Profiling Dashboard", layout="wide")

# Updated to render live url
API_URL = "https://the-haritz-ml-tool.onrender.com/predict-wallet-risk"

# 2. Title
st.markdown("# 🔍 Wallet Profiling Dashboard") # the emoji works as an icon :)

# 3. Sidebar filters
st.sidebar.header("FILTERS")
wallet_address = st.sidebar.text_input("Wallet Address", placeholder="Enter wallet address")
search_button = st.sidebar.button("Search")

# 4. Main logic: only fire when button clicked
if search_button and wallet_address:
    with st.spinner("Fetching risk profile..."):
        time.sleep(3)  # a lil delay don't hurt

        try:
            #Callinng backend
            resp = requests.post(API_URL, json={"wallet_address": wallet_address})
            if resp.status_code != 200:
                st.error(f"Backend error {resp.status_code}: {resp.text}")
                st.stop()

            data = resp.json()
            risk_score = data["risk_score"]
            risk_level_conf = data["risk_level"]
            timestamp_raw = data.get("timestamp", "")
            features = data.get("features", {})

            #label + color
            if risk_level_conf >= 70:
                risk_label, risk_color = "HIGH RISK", "red"
            elif risk_level_conf >= 40:
                risk_label, risk_color = "MEDIUM RISK", "gray"
            else:
                risk_label, risk_color = "LOW RISK", "green"

            #Format last active
            try:
                dt = datetime.fromisoformat(timestamp_raw.replace("Z", "+00:00"))
                days_ago = (datetime.now(timezone.utc) - dt).days
                last_active_display = f"{days_ago} days ago"
            except Exception:
                last_active_display = timestamp_raw

            #Header with wallet + badge
            st.markdown(f"""
<div style="display:flex; align-items:center; gap:10px;">
  <h3 style="margin:0;">{wallet_address[:6]}...{wallet_address[-4:]}</h3>
  <span style="
    background-color:{risk_color};
    color:white;
    padding:0.3em 0.8em;
    border-radius:0.5em;
    font-size:0.85em;
    font-weight:bold;">
    {risk_label}
  </span>
</div>
""", unsafe_allow_html=True)

            # Metric cards
            st.markdown(f"""
<div style="display:flex; gap:20px; flex-wrap:wrap;">
  <div style="border:2px solid {risk_color}; border-radius:10px; padding:1em; width:180px;">
    <h4 style="margin:0;">Risk Score</h4>
    <p style="font-size:1.5em; font-weight:bold; color:{risk_color};">{risk_score}</p>
  </div>
  <div style="border:1px solid #ccc; border-radius:10px; padding:1em; width:180px;">
    <h4 style="margin:0;">Total Transactions</h4>
    <p style="font-size:1.1em; font-weight:bold;">{int(features.get("total_transactions", 0))}</p>
  </div>
  <div style="border:1px solid #ccc; border-radius:10px; padding:1em; width:180px;">
    <h4 style="margin:0;">Avg. Fee</h4>
    <p style="font-size:1.5em; font-weight:bold;">{round(features.get("average_fee", 0), 6)}</p>
  </div>
  <div style="border:1px solid #ccc; border-radius:10px; padding:1em; width:180px;">
    <h4 style="margin:0;">Last Active</h4>
    <p style="font-size:1.2em; font-weight:bold;">{last_active_display}</p>
  </div>
  <div style="border:1px solid #ccc; border-radius:10px; padding:1em; width:180px;">
    <h4 style="margin:0;">Risk Level</h4>
    <p style="font-size:1.3em; font-weight:bold;">{risk_level_conf}%</p>
  </div>
</div>
""", unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("📊 Feature Summary")

            # Raw features table
            df = pd.DataFrame(list(features.items()), columns=["Feature", "Value"])
            st.dataframe(df, use_container_width=True)

            # Bar chart of numeric features
            numeric = {k: v for k, v in features.items() if isinstance(v, (int, float))}
            if numeric:
                chart_df = pd.DataFrame(numeric.items(), columns=["Feature", "Value"])
                chart = (
                    alt.Chart(chart_df)
                    .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
                    .encode(
                        x=alt.X("Feature:N", sort="-y", title=None),
                        y=alt.Y("Value:Q", title="Value"),
                        color=alt.value(risk_color),
                        tooltip=["Feature", "Value"],
                    )
                    .properties(width="container", height=350, title="🔎 Feature Distribution")
                    .configure_view(stroke=None)
                )
                st.altair_chart(chart, use_container_width=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")

elif search_button and not wallet_address:
    st.warning("Please enter a wallet address before searching.")
else:
    st.info("Enter a Solana wallet address to get started.")
