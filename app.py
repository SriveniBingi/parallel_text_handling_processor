import streamlit as st
import pandas as pd
import time
import multiprocessing
import matplotlib.pyplot as plt
import re

from config import POSITIVE_WORDS, NEGATIVE_WORDS, NEGATIONS, INTENSIFIERS, DB_NAME

# Backend modules
from processor import run_processing
from scorer import calculate_score
from database import fetch_all, insert_results, clear_table


# ================= PAGE CONFIG =================
st.set_page_config(page_title="ParaSense", page_icon="📊", layout="wide")

# ================= DARK THEME =================
# ================= SUBDUED BLUE THEME (MINIMAL SHADOW) =================
st.markdown("""
    <style>
    /* Global App Background */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar - Professional Dark */
    section[data-testid="stSidebar"] {
        background-color: #11141c !important;
        border-right: 1px solid #1f2937;
    }

    /* Metric Cards - Flat Professional Style */
    div[data-testid="stMetric"] {
        background: #161a23 !important;
        border: 1px solid #2d343f !important;
        padding: 20px !important;
        border-radius: 8px !important;
        box-shadow: none !important; /* Removed heavy shadow */
        transition: border-color 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: #0072ff !important;
    }

    /* Header Text */
    h1 {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    /* Buttons - Solid Blue with Minimal Shadow */
    .stButton>button {
        width: 100%;
        border-radius: 6px !important;
        height: 3em;
        background-color: #0072ff !important; /* Solid Blue */
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important; /* Very minimal shadow */
        transition: background-color 0.2s ease-in-out !important;
    }

    .stButton>button:hover {
        background-color: #0056cc !important; /* Darker blue on hover */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3) !important; /* Subtle lift */
        border: none !important;
    }

    /* Dataframe & Tables */
    .stDataFrame {
        border: 1px solid #1f2937;
        border-radius: 8px;
    }

    /* Input Fields */
    .stTextArea textarea, .stTextInput input {
        background-color: #161a23 !important;
        border: 1px solid #2d343f !important;
        color: #ffffff !important;
        border-radius: 6px !important;
    }

    /* Loading Spinner Color */
    .stSpinner > div {
        border-top-color: #0072ff !important;
    }
    </style>
""", unsafe_allow_html=True)


# ================= SESSION STATE =================
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Dashboard"
    
# ================= SIDEBAR NAVIGATION (LEFT SIDE) =================
with st.sidebar:
    st.title("🚀 Control Center")
    
   # 1.FILE UPLOAD 
    st.sidebar.markdown("🚀 Start by uploading your data file")

    uploaded_file = st.sidebar.file_uploader(
        "Upload File",
        type=["csv", "txt", "xlsx"]
    )
    
    st.divider()

    # 2. Navigation Radio Buttons
    st.markdown("### Navigation")
    active_tab = st.radio(
        "Select View",
        ["Dashboard", "Search", "Export", "Saved Results"],
        index=["Dashboard", "Search", "Export", "Saved Results"].index(st.session_state["active_tab"])
    )
    st.session_state["active_tab"] = active_tab


# ================= TITLE =================
st.title("📊 ParaSense")
st.caption("High-Velocity Parallel Text Analytics")
st.caption("Parallel Processing • Sentiment Analysis • Insights")


# Clear previous sentiment analysis results when new file is uploaded
if "sentiment_form" in st.session_state:
    del st.session_state["sentiment_form"]


# ================= TOP SENTIMENT ANALYZER (MANUAL) =================
st.subheader("🧮 Quick Sentiment Check")
with st.form("sentiment_form"):
    text_input = st.text_area("Enter text to test the logic:", placeholder="e.g., The service was not good but the food was amazing")
    col1, col2 = st.columns([1, 5])
    submit = col1.form_submit_button("Analyze")
    clear = col2.form_submit_button("Clear")

if submit and text_input:
    pos_count, neg_count, total_score, sentiment = calculate_score(text_input)

    cols = st.columns(4)
    cols[0].metric("Sentiment", sentiment)
    cols[1].metric("Positives", pos_count)
    cols[2].metric("Negatives", neg_count)
    cols[3].metric("Total Score", total_score)

st.divider()

# ================= FILE HANDLING =================
if uploaded_file:

    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "csv":
        df = pd.read_csv(uploaded_file, low_memory=False, engine="c")

    elif file_type == "xlsx":
        df = pd.read_excel(uploaded_file)

    elif file_type == "txt":
        # errors="ignore" prevents the 0xf1 Unicode error
        text = uploaded_file.read().decode("utf-8", errors="ignore").splitlines()
        df = pd.DataFrame({"text": text})
        
    # 2. DYNAMIC COLUMN MAPPING (Only happens once now)
    st.subheader("🎯 Data Configuration")
    all_cols = df.columns.tolist()
    
    # We use a unique key 'col_selector' to prevent Streamlit duplicate errors
    text_column = st.selectbox("Select Feedback/Text Column", all_cols, key="col_selector")
    
    # Rename and Clean
    df = df.rename(columns={text_column: "text"})
    df["text"] = df["text"].astype(str).fillna("").str.strip()

    # 3. MEMORY OPTIMIZATION (Critical for 1M Rows)
    # Downcast numeric columns to save RAM
    for col in df.columns:
        if df[col].dtype == 'float64':
            df[col] = pd.to_numeric(df[col], downcast='float')
        if df[col].dtype == 'int64':
            df[col] = pd.to_numeric(df[col], downcast='integer')
    
    if df.empty:
      st.error("⚠️ File has no data. Please upload a valid file.")
      st.stop()   
   
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

        # ✅ Better chunk size
        if len(data) < 1000:
            chunk_size = len(data)
        else:
           chunk_size = max(1, len(data) // (cores * 4))
        st.info(f"📦 Chunk Size: {chunk_size} | Cores: {cores}")

        # 🔹 NORMAL PROCESSING (ONLY FOR SMALL DATA)
        if len(data) < 10000:

            start_normal = time.time()

            normal_results = []
            for row in data:
                id, text = row
                pos, neg, score, sentiment = calculate_score(text)
                normal_results.append((id, text, score, sentiment))

            end_normal = time.time()

        else:
            st.info("Skipping normal processing for large dataset")

        # 🔹 PARALLEL PROCESSING
        start_parallel = time.time()

        with st.spinner("Processing... ⏳"):
            from database import clear_table
            clear_table()
            results = run_processing(data, chunk_size)

        end_parallel = time.time()

        st.success("Processing Completed ✅")
        #st.info(f"⚡ Parallel Time: {round(end_parallel - start_parallel, 2)} sec")

        # 🔹 PERFORMANCE COMPARISON
       
        if len(data) < 10000:
            st.subheader("⚡ Performance Comparison")
            st.write(f"Normal Processing Time: {round(end_normal - start_normal, 2)} sec")

            if (end_parallel - start_parallel) < (end_normal - start_normal):
                st.success("Parallel processing is faster 🚀")
            else:
                st.warning("Parallel processing slower for small data ⚠️")

        st.write(f"Parallel Processing Time: {round(end_parallel - start_parallel, 2)} sec")

        # 🔹 STORE RESULTS
        results_df = pd.DataFrame(
            results,
            columns=["id", "text", "score", "sentiment"]
        )

        # Optimization: Categorical types save ~80% RAM on 1M rows
        results_df["sentiment"] = results_df["sentiment"].astype("category")
        results_df["score"] = results_df["score"].astype("int16")
        
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

    # ================= DASHBOARD =================
    if active_tab == "Dashboard":
        st.subheader("⚡ Dashboard")
        st.divider()

        # --- 2️⃣ Overall Sentiment Charts for Processed Data ---
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

        # --- 3️⃣ Processed Data Table ---
        st.subheader("📊 Processed Data")
        st.dataframe(results_df)

    # ================= SEARCH =================
    elif active_tab == "Search":
        st.subheader("⚡ Search & Filter")

        keyword = st.text_input("Enter keywords or sentence", placeholder="Search here")
        filtered = results_df.copy()
        filtered["score"] = pd.to_numeric(filtered["score"], errors='coerce')
        
        if keyword.strip():
    
            clean_kw = keyword.lower().strip()

            # 🔥 If full sentence → strict match
            if len(clean_kw.split()) > 2:
                filtered = filtered[
                    filtered["text"].str.lower().str.contains(clean_kw, na=False)
                ]
            else:
                # 🔹 keyword search
                search_words = [
                    w for w in clean_kw.split()
                    if len(w) > 2
                ]

                if search_words:
                    pattern = "|".join(map(re.escape, search_words))
                    filtered = filtered[
                        filtered["text"].str.contains(pattern, case=False, na=False)
                    ]
                
            # ===== KEYWORD SENTIMENT =====
            pos_count, neg_count, total_score, sentiment = calculate_score(keyword)

            st.subheader("🧮 Keyword Sentiment Analysis")
            st.write(f"Positive Count: {pos_count}")
            st.write(f"Negative Count: {neg_count}")
            st.write(f"Total Score: {total_score}")
            st.write(f"Sentiment: {sentiment}")

        # ===== FILTERS =====
        sentiment_filter = st.selectbox(
            "Filter by Sentiment",
            ["All", "Positive", "Negative", "Neutral"]
        )

        if sentiment_filter != "All":
            filtered = filtered[filtered["sentiment"] == sentiment_filter]

        # ===== SCORE FILTER =====
        min_score = st.slider("Min Score", -10, 10, -10)
        if min_score != -10:
            filtered = filtered[filtered["score"] == min_score]
        else:
            filtered = filtered[filtered["score"] >= min_score]
        
        st.divider()
        
        # ===== DISPLAY =====
        st.info(f"🔍 {len(filtered)} results found")
        
        st.dataframe(filtered[["id", "text", "score", "sentiment"]],use_container_width=True)

        # ===== SAVE =====
        from database import insert_results

        if not filtered.empty and st.button("💾 Save Results"):
            st.session_state["saved_search"] = filtered
            insert_results(filtered[["id", "text", "score", "sentiment"]].values.tolist())
            st.toast("Results saved successfully ✅")
            
            
    # ================= EXPORT =================
    elif active_tab == "Export":
        st.subheader("⚡ Export Results")
        csv = results_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download CSV",
            csv,
            "results.csv",
            "text/csv"
            )

    # ================= SAVED RESULTS =================
    elif active_tab == "Saved Results":
        st.subheader("⚡ Saved Results")
        data = fetch_all()

        if data:
            df_saved = pd.DataFrame(data, columns=["id","text","score","sentiment"])
            st.dataframe(df_saved)
            
            # Move the button inside the 'if data' block
            st.download_button(
                label="💾 Download Saved Results",
                data=df_saved.to_csv(index=False).encode("utf-8"),
                file_name="saved_results.csv",
                mime="text/csv"
            )
        else:
            st.info("No saved results found in the database.")
            
# Reset Button (In Sidebar)
with st.sidebar:
    st.divider()
    if st.button("🔄 Reset"):
        st.session_state.clear()
        st.rerun()