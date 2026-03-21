import streamlit as st
import pandas as pd
import time
import multiprocessing
import matplotlib.pyplot as plt
import re

# Backend modules
from processor import run_processing
from database import clear_table


# ================= PAGE CONFIG =================
st.set_page_config(page_title="Text Analysis Dashboard", layout="wide")


# ================= DARK THEME =================
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #161a23;
        color: white;
    }

    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }

    .stMetric label, .stMetric div {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)


# ================= SESSION STATE =================
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Dashboard"


# ================= TITLE =================
st.title("📊 Text Analysis Dashboard")
st.caption("Parallel Processing • Sentiment Analysis • Insights")


# ================= FILE UPLOAD =================
st.sidebar.markdown("🚀 Start by uploading your data file")

uploaded_file = st.sidebar.file_uploader(
    "Upload File",
    type=["csv", "txt", "xlsx"]
)


# ================= SENTIMENT SCORER =================
def calculate_score(text):
    positive_words = ["good", "excellent", "great", "awesome", "happy"]
    negative_words = ["bad", "poor", "worst", "sad", "terrible"]

    words = text.lower().split()

    scores = []
    for word in words:
        if word in positive_words:
            scores.append(1)
        elif word in negative_words:
            scores.append(-1)

    total_score = sum(scores)

    if total_score > 0:
        sentiment = "Positive"
    elif total_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return scores, total_score, sentiment


# ================= FILE HANDLING =================
if uploaded_file:

    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "csv":
        df = pd.read_csv(uploaded_file)

    elif file_type == "xlsx":
        df = pd.read_excel(uploaded_file)

    elif file_type == "txt":
        text = uploaded_file.read().decode("utf-8").splitlines()
        df = pd.DataFrame({"text": text})

    # ===== PREVIEW =====
    st.subheader("📄 Data Preview")
    if len(df) > 100:
        st.caption("Showing first 100 sentences/rows")
    st.dataframe(df.head(100))

    st.divider()

    # ===== COLUMN SELECTION =====
    if file_type in ["csv", "xlsx"]:
        text_columns = df.select_dtypes(include=["object"]).columns

        if len(text_columns) == 0:
            st.error("No text columns found ❌")
            st.stop()

        text_column = st.selectbox("Select Text Column", text_columns)
        df = df.rename(columns={text_column: "text"})

    # ===== LIMIT LARGE DATA =====
    MAX_ROWS = 100000

    if len(df) > 50000:
        st.warning("⚠️ Large dataset detected")

    if len(df) > MAX_ROWS:
        st.warning(f"⚠️ Limiting to first {MAX_ROWS} rows")
        df = df.head(MAX_ROWS)

    # ===== PROCESS BUTTON =====
    if st.button("🚀 Start Processing"):

        if df.empty:
            st.error("No valid data ❌")
            st.stop()

        df["id"] = range(len(df))
        data = list(df[["id", "text"]].itertuples(index=False, name=None))

        cores = multiprocessing.cpu_count()
        chunk_size = max(1000, len(data) // cores)

        st.info(f"📦 Chunk Size: {chunk_size} | Cores: {cores}")

        start = time.time()

        with st.spinner("Processing... ⏳"):
            results = run_processing(data, chunk_size)

        end = time.time()

        st.success("Processing Completed ✅")
        st.info(f"⚡ Execution Time: {round(end - start, 2)} sec")

        results_df = pd.DataFrame(
            results,
            columns=["id", "text", "score", "sentiment"]
        )

        st.session_state["results_df"] = results_df


# ================= RESULTS =================
if "results_df" in st.session_state:

    results_df = st.session_state["results_df"]

    total = len(results_df)
    pos = (results_df["sentiment"] == "Positive").sum()
    neg = (results_df["sentiment"] == "Negative").sum()
    neu = (results_df["sentiment"] == "Neutral").sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total", total)
    c2.metric("Positive", pos)
    c3.metric("Negative", neg)
    c4.metric("Neutral", neu)

    st.divider()

    tabs = ["Dashboard", "Search", "Export", "Saved Results"]

    active_tab = st.radio(
        "Navigate",
        tabs,
        horizontal=True,
        index=tabs.index(st.session_state["active_tab"])
    )

    st.session_state["active_tab"] = active_tab

    # ================= DASHBOARD =================
    if active_tab == "Dashboard":

        chart_df = pd.DataFrame({
            "Sentiment": ["Positive", "Negative", "Neutral"],
            "Count": [pos, neg, neu]
        })

        colA, colB = st.columns(2)

        with colA:
            fig1, ax1 = plt.subplots()
            chart_df.set_index("Sentiment").plot(kind="bar", ax=ax1)
            st.pyplot(fig1)

        with colB:
            fig2, ax2 = plt.subplots()
            ax2.pie(chart_df["Count"], labels=chart_df["Sentiment"], autopct="%1.1f%%")
            st.pyplot(fig2)

        st.subheader("📊 Processed Data")
        st.dataframe(results_df)

        st.subheader("🚨 Negative Alerts")

        alerts = results_df[results_df["sentiment"] == "Negative"]

        if not alerts.empty:
            for _, row in alerts.head(5).iterrows():
                st.error(row["text"])
        else:
            st.success("No negative feedback 🎉")

    # ================= SEARCH =================
    elif active_tab == "Search":

        keyword = st.text_input("Enter keywords")

        if keyword.strip():
            scores, total_score, sentiment = calculate_score(keyword)

            st.subheader("🧮 Keyword Sentiment Analysis")
            st.write(f"Scores: {scores}")
            st.write(f"Total Score: {total_score}")
            st.write(f"Sentiment: {sentiment}")

        sentiment_filter = st.selectbox(
            "Filter",
            ["All", "Positive", "Negative", "Neutral"]
        )

        min_score = st.slider("Min Score", -5, 5, -5)

        start_search = time.time()

        filtered = results_df.copy()

        if keyword.strip():
            words = list(set(keyword.lower().split()))
            pattern = "|".join(map(re.escape, words))

            filtered = filtered[
                filtered["text"].str.lower().str.contains(pattern, regex=True)
            ]

        if sentiment_filter != "All":
            filtered = filtered[
                filtered["sentiment"] == sentiment_filter
            ]

        filtered = filtered[filtered["score"] >= min_score]

        end_search = time.time()

        st.info(f"🔍 Search Time: {round(end_search - start_search, 3)} sec")

        if filtered.empty:
            st.warning("No results found")
        else:
            st.dataframe(filtered)

        if st.button("💾 Save Results"):
            st.session_state["saved_search"] = filtered
            st.toast("Results saved successfully ✅")

    # ================= EXPORT =================
    elif active_tab == "Export":

        csv = results_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download CSV",
            csv,
            "results.csv",
            "text/csv"
        )

    # ================= SAVED RESULTS =================
    elif active_tab == "Saved Results":

        if "saved_search" in st.session_state:
            st.dataframe(st.session_state["saved_search"])
        else:
            st.info("No saved results")

    # ================= RESET & CLEAR =================
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Reset"):
            st.session_state.clear()
            st.rerun()

    with col2:
        if st.button("🗑️ Clear Database"):
            clear_table()
            st.toast("Database cleared successfully ✅")