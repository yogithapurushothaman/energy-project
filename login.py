import streamlit as st
import pandas as pd
import numpy as np
import time

# 🔐 LOGIN CHECK
if not st.session_state.get("logged_in"):
    st.warning("🔐 Please login first")
    st.stop()

# Page config
st.set_page_config(page_title="Smart Energy Dashboard", layout="wide")

st.title("⚡ AI Digital Twin Smart Energy Command Center")
st.markdown("---")

# 📂 FILE UPLOAD
st.sidebar.title("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset", type=["csv", "xlsx"]
)

if uploaded_file is not None:
    file_name = uploaded_file.name

    if file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    else:
        st.error("Unsupported file format")
        st.stop()

else:
    st.warning("Please upload a dataset")
    st.stop()

# ✅ REQUIRED COLUMN CHECK
if 'MW' not in df.columns:
    st.error("Dataset must contain 'MW' column")
    st.stop()

# 🔁 SIMULATE LIVE DATA
new_row = df.iloc[-1].copy()
new_row['MW'] += np.random.uniform(-0.5, 0.5)

if 'HZ' in df.columns:
    new_row['HZ'] += np.random.uniform(-0.05, 0.05)

df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# ✅ LIMIT DATA
df = df.tail(50)

# 🔹 DIGITAL TWIN
df['T1'] = df['MW'] * 0.20
df['T2'] = df['MW'] * 0.25
df['T3'] = df['MW'] * 0.15
df['T4'] = df['MW'] * 0.20
df['T5'] = df['MW'] * 0.20

# 🔹 AI RISK FUNCTION
def check_risk(x):
    if x > 1.0:
        return "CRITICAL"
    elif x > 0.7:
        return "WARNING"
    else:
        return "SAFE"

for t in ['T1','T2','T3','T4','T5']:
    df[t + '_status'] = df[t].apply(check_risk)

# 🔹 METRICS
avg_load = df['MW'].mean()
max_load = df['MW'].max()
min_load = df['MW'].min()

col1, col2, col3 = st.columns(3)
col1.metric("⚡ Avg Load (MW)", round(avg_load, 2))
col2.metric("🔺 Max Load (MW)", round(max_load, 2))
col3.metric("🔻 Min Load (MW)", round(min_load, 2))

st.markdown("---")

# 🔹 SYSTEM STATUS
st.subheader("🚨 Live System Status")

critical_count = (df[[t+'_status' for t in ['T1','T2','T3','T4','T5']]] == "CRITICAL").sum().sum()
warning_count = (df[[t+'_status' for t in ['T1','T2','T3','T4','T5']]] == "WARNING").sum().sum()

if critical_count > 5:
    st.error(f"⚠️ CRITICAL: {critical_count} overload events detected!")
elif warning_count > 5:
    st.warning(f"⚡ WARNING: {warning_count} stress events detected")
else:
    st.success("✅ System Stable")

# 📊 GRAPH
st.subheader("📊 Energy Load")
st.line_chart(df['MW'])

st.markdown("---")

# ⚡ TRANSFORMER DATA
st.subheader("⚡ Transformer Monitoring")

col1, col2 = st.columns(2)

with col1:
    st.dataframe(df[['T1','T2','T3','T4','T5']])

with col2:
    st.dataframe(df[['T1_status','T2_status','T3_status','T4_status','T5_status']])

st.markdown("---")

# 🔥 AI SCENARIO
st.subheader("🔥 AI Scenario Detection")

if max_load > 4.5:
    st.error("🔥 Heatwave Condition Detected")
elif avg_load > 3.5:
    st.warning("⚡ Peak Demand Period")
else:
    st.success("✅ Normal Condition")

# 🧠 ANOMALY DETECTION
st.subheader("🧠 Anomaly Detection")

spikes = df[df['MW'] > (avg_load + 2*df['MW'].std())]

if not spikes.empty:
    st.warning(f"⚡ {len(spikes)} abnormal spikes detected")
else:
    st.success("✅ No anomalies")

# ⚠️ PROBLEM DETECTION
st.subheader("⚠️ Problem Detection")

for t in ['T1','T2','T3','T4','T5']:
    status = df[t + '_status'].iloc[-1]

    if status == "CRITICAL":
        st.error(f"{t}: Overloaded 🚨")
    elif status == "WARNING":
        st.warning(f"{t}: High load ⚠️")
    else:
        st.success(f"{t}: Normal ✅")

# 🛠️ SOLUTIONS
st.subheader("🛠️ Suggested Solutions")

for t in ['T1','T2','T3','T4','T5']:
    status = df[t + '_status'].iloc[-1]

    if status == "CRITICAL":
        st.error(f"{t}: Reduce load immediately | Maintenance needed")
    elif status == "WARNING":
        st.warning(f"{t}: Monitor & balance load")
    else:
        st.success(f"{t}: No action needed")

# 🏙️ CONTROL CENTER
st.subheader("🏙️ Smart Grid Control Center")

if critical_count > 0:
    st.error("🚨 Grid Risk: HIGH")
elif warning_count > 0:
    st.warning("⚡ Grid Risk: MEDIUM")
else:
    st.success("✅ Grid Risk: LOW")

# 🔓 LOGOUT BUTTON
st.sidebar.markdown("---")
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

st.markdown("---")
st.caption("AI-Driven Digital Twin | Smart Energy Monitoring 🚀")

# 🔁 AUTO REFRESH
time.sleep(10)
st.rerun()