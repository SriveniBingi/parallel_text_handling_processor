import streamlit as st
import pandas as pd
import time
import multiprocessing
import matplotlib.pyplot as plt
from processor import run_processing

# ================= CONFIG =================
st.set_page_config(page_title="Text Analysis Dashboard", layout="wide")

# Title
st.title("📊 Text Analysis Dashboard")
st.caption("Parallel Processing • Sentiment Analysis • Insights")

start_button = False  # Prevent undefined error

# ================= SIDEBAR =================

uploaded_file = st.sidebar.file_uploader(
    "Upload File",
    type=["csv", "txt", "xlsx"]
)

# ================= FILE HANDLING =================
if uploaded_file:

    file_type = uploaded_file.name.split(".")[-1]

    # ---------- CSV ----------
    if file_type == "csv":
        df = pd.read_csv(uploaded_file)

    # ---------- Excel ----------
    elif file_type == "xlsx":
        df = pd.read_excel(uploaded_file)

    # ---------- TXT ----------
    elif file_type == "txt":
        text = uploaded_file.read().decode("utf-8").splitlines()
        df = pd.DataFrame({"text": text})
        
        # Remove empty rows
        df["text"] = df["text"].astype(str).str.strip()
        df = df[df["text"] != ""]

    if len(df) > 50000:
        st.warning("⚠️ Processing 50K+ records. This may take some time.")

    # Preview
    st.subheader("📄 Data Preview")
    
    if len(df) > 1000:
        st.warning("⚠️ Large dataset detected. Showing first 100 rows only.")
        st.dataframe(df.head(100))
    else:
        st.dataframe(df)

    st.divider()

    # ================= COLUMN SELECTION =================
    if file_type in ["csv", "xlsx"]:

        st.subheader("⚙️ Select Text Column")

        # Select only text columns
        text_columns = df.select_dtypes(include=["object"]).columns

        if len(text_columns) == 0:
           st.error("No text columns found ❌")
           st.stop()

        text_column = st.selectbox( "Choose column for analysis",text_columns)

        df = df.rename(columns={text_column: "text"})

        start_button = st.button("🚀 Start Processing")

    else:
        start_button = st.button("🚀 Start Processing")

    # ================= PROCESSING =================
    if start_button:
        progress = st.progress(0)
        progress.progress(20)

        if "text" not in df.columns:
            st.error("No text column found ❌")
            st.stop()
            
        df["text"] = df["text"].astype(str).str.strip()
        df = df[df["text"] != ""]

        if df.empty:
            st.error("❌ No valid text data found in selected column.")
            st.stop()

        if "id" not in df.columns:
            df["id"] = range(len(df))

            # Convert to list
    
        data = list(df[["id", "text"]].itertuples(index=False, name=None))
        
        if len(data) == 0:
           st.error("❌ No data available to process. Please upload a valid file.")
           st.stop()
        # ================= AUTO CHUNK SIZE =================
        data_size = len(data)
        cores = multiprocessing.cpu_count()

        chunk_size = max(50, data_size // (cores * 2))

        st.info(f"📦 Auto Chunk Size: {chunk_size} | Data Size: {data_size}")
        start_time = time.time()

        # ✅ Spinner added
        with st.spinner("Processing data... please wait ⏳"):
            results = run_processing(data, chunk_size)

        progress.progress(80)

        end_time = time.time()
        total_time = round(end_time - start_time, 2)
        cores_used = multiprocessing.cpu_count()

        progress.progress(100)

        st.success("Processing Completed ✅")
        st.info(f"⚡ Processed in {total_time}s using {cores_used} cores")

        results_df = pd.DataFrame(
            results,
            columns=["id", "text", "score", "sentiment"]
        )

        st.session_state["results_df"] = results_df
        st.info(f"Processed {len(results_df)} records successfully 🚀")

# ================= LOAD RESULTS =================
if "results_df" in st.session_state:

    results_df = st.session_state["results_df"]

    # ================= METRICS =================
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

    # ================= TABS =================
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Dashboard", "Search", "Export", "Saved Results"]
    )

    # ================= DASHBOARD =================
    with tab1:

        st.subheader("📊 Analysis Dashboard")

        chart_df = pd.DataFrame({
            "Sentiment": ["Positive", "Negative", "Neutral"],
            "Count": [pos, neg, neu]
        })

        colA, colB = st.columns(2)

        # Bar Chart
        with colA:
            fig1, ax1 = plt.subplots(figsize=(4, 3))
            chart_df.set_index("Sentiment").plot(kind="bar", ax=ax1)
            st.pyplot(fig1)

        # Pie Chart
        with colB:
            fig2, ax2 = plt.subplots(figsize=(4, 3))
            ax2.pie(chart_df["Count"], labels=chart_df["Sentiment"], autopct="%1.1f%%")
            st.pyplot(fig2)

        st.subheader("📋 Processed Data")
        st.dataframe(results_df)

    # ================= SEARCH =================
    with tab2:

        st.subheader("🔍 Search & Filter")

        keyword = st.text_input("Search keyword")

        sentiment_filter = st.selectbox(
            "Filter by Sentiment",
            ["All", "Positive", "Negative", "Neutral"]
        )

        min_score = st.slider("Minimum Score", -5, 5, -5)

        filtered = results_df.copy()

        if keyword:
            filtered = filtered[
                filtered["text"].str.contains(keyword, case=False)
            ]

        if sentiment_filter != "All":
            filtered = filtered[
                filtered["sentiment"] == sentiment_filter
            ]

        filtered = filtered[
            filtered["score"] >= min_score
        ]

        if filtered.empty:
            st.warning("No matching results found 🔍")
        else:
            st.dataframe(filtered)

        if st.button("💾 Save Search Results"):
            st.session_state["saved_search"] = filtered
            if not filtered.empty:
                st.success(f"✅ {len(filtered)} results saved successfully!")
            else:
                st.warning("No results to save ⚠️")

    # ================= EXPORT =================
    with tab3:

        st.subheader("📥 Export Data")

        csv = results_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Processed CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv"
        )

    # ================= SAVED RESULTS =================
    with tab4:

        st.subheader("📌 Saved Search Results")

        if "saved_search" in st.session_state:
            st.dataframe(st.session_state["saved_search"])
        else:
            st.info("No saved results yet")

    # ================= ALERTS =================
    st.subheader("🚨 Critical Negative Feedback Alerts")

    alerts = results_df[results_df["sentiment"] == "Negative"]

    st.write(f"Total Negative Feedback: {len(alerts)}")

    if not alerts.empty:
        for _, row in alerts.head(5).iterrows():
            st.error(f"🔴 {row['text']}")
    else:
        st.success("No negative feedback found 🎉")

# ================= FOOTER =================
st.divider()
st.caption("Developed for Parallel Text Processing Project 🚀")