import streamlit as st
import pandas as pd

import pandas as pd
import matplotlib.pyplot as plt

# STEP 1: LOAD DATA
file_path = "data.xls"
df = pd.read_excel(file_path)

# STEP 2: CHECK COLUMNS
print("Columns in your file:")
print(df.columns)

# STEP 3: SELECT IMPORTANT COLUMNS
df = df[['SYSTEMRTC', 'MW', 'MVAR', 'HZ', 'IPF']]

# STEP 4: CONVERT TIME
df['SYSTEMRTC'] = pd.to_datetime(df['SYSTEMRTC'])

# STEP 5: CLEAN DATA
df = df.dropna()

# STEP 6: SORT DATA
df = df.sort_values(by='SYSTEMRTC')

# STEP 7: RESET INDEX
df = df.reset_index(drop=True)

# STEP 8: SCALE MW (IMPORTANT)
df['MW'] = abs(df['MW'] * 1000)

# STEP 9: PRINT DATA
print("\nCleaned Data:")
print(df.head())

# STEP 10: PLOT GRAPH
plt.figure(figsize=(10,5))
plt.plot(df['SYSTEMRTC'], df['MW'], color='blue')
plt.xlabel("Time")
plt.ylabel("Load (MW)")
plt.title("Energy Load Over Time")
plt.show()
# STEP 11: CREATE DIGITAL TWIN (TRANSFORMERS)

# Create 5 transformers by splitting load
df['T1'] = df['MW'] * 0.20
df['T2'] = df['MW'] * 0.25
df['T3'] = df['MW'] * 0.15
df['T4'] = df['MW'] * 0.20
df['T5'] = df['MW'] * 0.20

# Show transformer data
print("\nTransformer Data:")
print(df[['SYSTEMRTC', 'T1', 'T2', 'T3', 'T4', 'T5']].head())
# STEP 11: CREATE DIGITAL TWIN (TRANSFORMERS)

df['T1'] = df['MW'] * 0.20
df['T2'] = df['MW'] * 0.25
df['T3'] = df['MW'] * 0.15
df['T4'] = df['MW'] * 0.20
df['T5'] = df['MW'] * 0.20

print("\nTransformer Data:")
print(df[['SYSTEMRTC', 'T1', 'T2', 'T3', 'T4', 'T5']].head())# STEP 12: RISK DETECTION

def check_risk(load):
    if load > 0.9:
        return "CRITICAL"
    elif load > 0.8:
        return "WARNING"
    else:
        return "SAFE"

# Apply risk logic to each transformer
df['T1_status'] = df['T1'].apply(check_risk)
df['T2_status'] = df['T2'].apply(check_risk)
df['T3_status'] = df['T3'].apply(check_risk)
df['T4_status'] = df['T4'].apply(check_risk)
df['T5_status'] = df['T5'].apply(check_risk)

# Show results
print("\nTransformer Risk Status:")
print(df[['SYSTEMRTC', 'T1_status', 'T2_status', 'T3_status', 'T4_status', 'T5_status']].head())
# STEP 12: RISK DETECTION

def check_risk(load):
    if load > 0.9:
        return "CRITICAL"
    elif load > 0.8:
        return "WARNING"
    else:
        return "SAFE"

# Apply risk logic to each transformer
df['T1_status'] = df['T1'].apply(check_risk)
df['T2_status'] = df['T2'].apply(check_risk)
df['T3_status'] = df['T3'].apply(check_risk)
df['T4_status'] = df['T4'].apply(check_risk)
df['T5_status'] = df['T5'].apply(check_risk)

# Show results
print("\nTransformer Risk Status:")
print(df[['SYSTEMRTC', 'T1_status', 'T2_status', 'T3_status', 'T4_status', 'T5_status']].head())
# STEP 13: SCENARIO SIMULATION (HEATWAVE)

# Create a copy of data for simulation
df_sim = df.copy()

# Increase load by 30% (simulate heatwave)
df_sim['MW'] = df_sim['MW'] * 1.3

# Recalculate transformers
df_sim['T1'] = df_sim['MW'] * 0.20
df_sim['T2'] = df_sim['MW'] * 0.25
df_sim['T3'] = df_sim['MW'] * 0.15
df_sim['T4'] = df_sim['MW'] * 0.20
df_sim['T5'] = df_sim['MW'] * 0.20

# Apply risk again
df_sim['T1_status'] = df_sim['T1'].apply(check_risk)
df_sim['T2_status'] = df_sim['T2'].apply(check_risk)
df_sim['T3_status'] = df_sim['T3'].apply(check_risk)
df_sim['T4_status'] = df_sim['T4'].apply(check_risk)
df_sim['T5_status'] = df_sim['T5'].apply(check_risk)

# Show simulation result
print("\n🔥 HEATWAVE SIMULATION RESULT:")
print(df_sim[['SYSTEMRTC', 'T1_status', 'T2_status', 'T3_status', 'T4_status', 'T5_status']].head())
# SAVE FINAL DATA FOR DASHBOARD
df.to_csv("final_output.csv", index=False)
st.subheader("🚨 Emergency Scenario")

st.write("Transformer Failure Simulation")
st.error("⚠️ Load redistributed → nearby transformers at risk")
st.subheader("📂 Upload New Dataset")

uploaded_file = st.file_uploader("Upload Excel File", type=["xls", "xlsx", "csv"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success("✅ New dataset loaded successfully!")

else:
    df = pd.read_csv("final_output.csv")