import streamlit as st
import pandas as pd
from processor import run_processing

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Feedback Dashboard", layout="wide")

# ---------- TITLE ----------
st.title("📊 Student Feedback Analytics")
st.caption("Parallel Processing + Sentiment Insights 🚀")

# ---------- SIDEBAR ----------
st.sidebar.header("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload CSV File",
    type=["csv"]
)

start_button = st.sidebar.button("🚀 Start Processing")

# ---------- FILE PREVIEW ----------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📂 File Preview")
    st.dataframe(df.head(), use_container_width=True)

# ---------- PROCESSING ----------
if uploaded_file is not None and start_button:

    st.subheader("⚙️ Processing Status")

    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)

    # Convert dataframe → list of tuples
    data = list(df.itertuples(index=False, name=None))

    results = run_processing(data)

    st.success("✅ Processing Completed")

    # Convert results → DataFrame
    results_df = pd.DataFrame(
        results,
        columns=["ID", "Name", "Feedback", "Score", "Sentiment"]
    )

    # ---------- METRICS ----------
    total = len(results_df)
    positive = (results_df["Sentiment"] == "Positive").sum()
    negative = (results_df["Sentiment"] == "Negative").sum()
    neutral = (results_df["Sentiment"] == "Neutral").sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📁 Total", total)
    col2.metric("😊 Positive", positive)
    col3.metric("😡 Negative", negative)
    col4.metric("😐 Neutral", neutral)

    # ---------- TABS ----------
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔍 Search & Filter", "⬇ Export"])

    # ===== TAB 1: DASHBOARD =====
    with tab1:
        st.subheader("📊 Results Overview")

        st.dataframe(results_df, use_container_width=True)

        # Charts
        chart_data = pd.DataFrame({
            "Sentiment": ["Positive", "Negative", "Neutral"],
            "Count": [positive, negative, neutral]
        })

        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(chart_data.set_index("Sentiment"))

        with col2:
            st.write("### 🥧 Sentiment Distribution")
            st.pyplot(chart_data.set_index("Sentiment").plot.pie(
                y="Count", autopct='%1.1f%%'
            ).figure)

    # ===== TAB 2: SEARCH =====
    with tab2:
        st.subheader("🔍 Search & Filter")

        keyword = st.text_input("Search by keyword")

        sentiment_filter = st.selectbox(
            "Filter by Sentiment",
            ["All", "Positive", "Negative", "Neutral"]
        )

        filtered = results_df.copy()

        if sentiment_filter != "All":
            filtered = filtered[
                filtered["Sentiment"] == sentiment_filter
            ]

        if keyword:
            filtered = filtered[
                filtered["Feedback"].str.contains(keyword, case=False)
            ]

        st.dataframe(filtered, use_container_width=True)

    # ===== TAB 3: EXPORT =====
    with tab3:
        st.subheader("⬇ Export Data")

        # Full data
        csv_all = results_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Full Data",
            csv_all,
            "all_results.csv"
        )

        # Filtered data
        csv_filtered = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Filtered Data",
            csv_filtered,
            "filtered_results.csv"
        )

    # ---------- ALERTS ----------
    st.subheader("⚠️ Negative Feedback Alerts")

    alerts = results_df[results_df["Sentiment"] == "Negative"]

    if not alerts.empty:
        for _, row in alerts.head(5).iterrows():
            st.warning(f"{row['Name']} → {row['Feedback']}")
    else:
        st.success("No negative feedback 🎉")