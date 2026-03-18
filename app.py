import streamlit as st
import pandas as pd
import time
import multiprocessing
import matplotlib.pyplot as plt
from processor import run_processing

# Page config
st.set_page_config(page_title="AI Feedback Dashboard", layout="wide")

# Title
st.title("🤖 Student Feedback Dashboard")
st.caption("Sentiment Analysis + Parallel Processing 🚀")

# Sidebar
st.sidebar.header("Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
start_button = st.sidebar.button("Start Processing")

# ================= FILE UPLOAD =================
if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Preview")
    st.dataframe(df)

    # ================= PROCESSING =================
    if start_button:

        progress = st.progress(0)
        progress.progress(20)

        data = list(df.itertuples(index=False, name=None))

        start_time = time.time()
        results = run_processing(data)
        progress.progress(80)

        end_time = time.time()
        total_time = round(end_time - start_time, 2)
        cores_used = multiprocessing.cpu_count()

        progress.progress(100)

        st.success("Processing Completed ✅")
        st.info(f"Processed in {total_time} seconds using {cores_used} cores 🚀")

        results_df = pd.DataFrame(
            results,
            columns=["student_id", "student_name", "feedback", "score", "sentiment"]
        )

        # ✅ SAVE RESULTS
        st.session_state["results_df"] = results_df

# ================= LOAD SAVED RESULTS =================
if "results_df" in st.session_state:

    results_df = st.session_state["results_df"]

    # Metrics
    total = len(results_df)
    pos = (results_df["sentiment"] == "Positive").sum()
    neg = (results_df["sentiment"] == "Negative").sum()
    neu = (results_df["sentiment"] == "Neutral").sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", total)
    col2.metric("Positive", pos)
    col3.metric("Negative", neg)
    col4.metric("Neutral", neu)

    st.divider()

    # Tabs
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Search", "Export"])

    # ================= DASHBOARD =================
    with tab1:

        st.subheader("📊 Sentiment Analysis Dashboard")

        chart_df = pd.DataFrame({
            "Sentiment": ["Positive", "Negative", "Neutral"],
            "Count": [pos, neg, neu]
        })

        colA, colB = st.columns(2)

        # Small Bar Chart
        with colA:
            fig1, ax1 = plt.subplots(figsize=(4, 3))
            chart_df.set_index("Sentiment").plot(kind="bar", ax=ax1)
            ax1.set_title("Counts")
            st.pyplot(fig1)

        # Small Pie Chart
        with colB:
            fig2, ax2 = plt.subplots(figsize=(4, 3))
            ax2.pie(chart_df["Count"], labels=chart_df["Sentiment"], autopct="%1.1f%%")
            ax2.set_title("Distribution")
            st.pyplot(fig2)

        st.subheader("📋 Processed Data")
        st.dataframe(results_df)

    # ================= SEARCH =================
    with tab2:

        st.subheader("🔍 Search Feedback")

        keyword = st.text_input("Enter keyword")

        if keyword:
            filtered = results_df[
                results_df["feedback"].str.contains(keyword, case=False)
            ]
            st.dataframe(filtered)
        else:
            st.info("Enter a keyword to search")

    # ================= EXPORT =================
    with tab3:

        st.subheader("📥 Export Data")

        csv = results_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Processed CSV",
            data=csv,
            file_name="processed_feedback.csv",
            mime="text/csv"
        )

    # ================= ALERTS =================
    st.subheader("⚠️ Negative Alerts")

    alerts = results_df[results_df["sentiment"] == "Negative"]

    if not alerts.empty:
        for _, row in alerts.head(5).iterrows():
            st.error(f"🔴 {row['student_name']} → {row['feedback']}")
    else:
        st.success("No negative feedback found 🎉")