import streamlit as st
import pandas as pd

st.set_page_config(page_title="Verified Advanced Recruiting Portal", layout="wide")

st.title("🎯 Verified Advanced Recruiting Analytics Portal")

uploaded_files = st.file_uploader("Upload TrackMan CSV(s)", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    df_list = [pd.read_csv(file) for file in uploaded_files]
    df = pd.concat(df_list, ignore_index=True)

    st.subheader("Player Metrics (Raw Data)")
    st.write(df.head())

    # Group by player and average metrics
    # Replace 'PlayerName' with the actual column name for player identifier in your CSV
    player_id_col = "Pitcher"  # Change this if your column is named differently
    pitch_type_col = "TaggedPitchType"  # Change this if your column is named differently
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    avg_df = df.groupby([player_id_col, pitch_type_col])[numeric_cols].mean().reset_index()

    st.subheader("Average Player Metrics")
    st.write(avg_df)

    # Example filters (you’ll expand later)
    pitch_type = st.selectbox("Select Pitch Type", avg_df[pitch_type_col].unique())
    min_spin = st.slider("Minimum Spin Rate (RPM)", 0, 3500, 2000)
    min_hbreak = st.slider("Minimum Horizontal Break (in)", -30, 30, 10)
    min_vbreak = st.slider("Minimum Vertical Break (in)", -60, 60, 10)

    filtered = avg_df[
        (avg_df[pitch_type_col] == pitch_type) &
        (avg_df['SpinRate'] >= min_spin) &
        (avg_df['HorzBreak'] >= min_hbreak) &
        (avg_df['VertBreak'] >= min_vbreak)
    ]

    display_cols = [player_id_col, pitch_type_col, "RelSpeed", "SpinRate", "SpinAxis", "Extension", "VertBreak", "HorzBreak"]
    filtered_display = filtered[display_cols]

    st.subheader("Filtered Players")
    st.write(filtered_display)
