import streamlit as st
import pandas as pd
import time
import multiprocessing
import matplotlib.pyplot as plt
import re
from config import POSITIVE_WORDS, NEGATIVE_WORDS, NEGATIONS, INTENSIFIERS, DB_NAME

# Backend modules
from processor import run_processing
from database import fetch_all, insert_results, clear_table


# ================= PAGE CONFIG =================
st.set_page_config(page_title="ParaSense", page_icon="📊", layout="wide")

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


# ================= SENTIMENT SCORER =================
def calculate_score(text):

    words = text.lower().split()

    total_score = 0
    pos_count = 0
    neg_count = 0

    i = 0
    while i < len(words):
        word = words[i]

        multiplier = 1
        invert = False

        # Check for negation
        if word in NEGATIONS and i + 1 < len(words):
            invert = True
            i += 1
            word = words[i]

        # Check for intensifier
        if word in INTENSIFIERS and i + 1 < len(words):
            multiplier = 2
            i += 1
            word = words[i]

        # Apply scoring
        if word in POSITIVE_WORDS:
            score = 1 * multiplier
            if invert:
                score *= -1
            total_score += score
            pos_count += 1

        elif word in NEGATIVE_WORDS:
            score = -1 * multiplier
            if invert:
                score *= -1
            total_score += score
            neg_count += 1
            #display as negative

        i += 1

    # Final sentiment
    if total_score > 0:
        sentiment = "Positive"
    elif total_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return pos_count, neg_count, total_score, sentiment

# ================= TOP SENTIMENT ANALYZER (MANUAL) =================
st.subheader("🧮 Quick Sentiment Check")
with st.form("sentiment_form"):
    text_input = st.text_area("Enter text to test the logic:", placeholder="e.g., The service was not good but the food was amazing")
    col1, col2 = st.columns([1, 5])
    submit = col1.form_submit_button("Analyze")
    clear = col2.form_submit_button("Clear")

if submit and text_input:
    p, n, s, sent = calculate_score(text_input)
    cols = st.columns(4)
    cols[0].metric("Sentiment", sent)
    cols[1].metric("Positives", p)
    cols[2].metric("Negatives", n)
    cols[3].metric("Total Score", s)


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
    
    if df.empty:
      st.error("⚠️ File has no data. Please upload a valid file.")
      st.stop()    

    # ===== PREVIEW =====
    st.subheader("📄 Data Preview")
    if len(df) > 100:
        st.caption("Showing first 5 sentences/rows")
    st.dataframe(df.head(5))

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
            POS = {"good", "excellent", "great", "awesome", "happy"}
            NEG = {"bad", "poor", "worst", "sad", "terrible"}
            for row in data:
                id, text = row

                score = 0
                words = text.lower().split()

                for word in words:
                    if word in POS:
                        score += 1
                    elif word in NEG:
                        score -= 1

                if score > 0:
                    sentiment = "Positive"
                elif score < 0:
                    sentiment = "Negative"
                else:
                    sentiment = "Neutral"

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
        st.info(f"⚡ Parallel Time: {round(end_parallel - start_parallel, 2)} sec")

        # 🔹 PERFORMANCE COMPARISON
        st.subheader("⚡ Performance Comparison")

        if len(data) < 10000:
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
        keyword = st.text_input("Enter keywords")

        if keyword.strip():
            pos_count, neg_count, total_score, sentiment = calculate_score(keyword)

            st.subheader("🧮 Keyword Sentiment Analysis")
            st.write(f"Positive Count: {pos_count}")
            st.write(f"Negative Count: {-neg_count}")
            st.write(f"Total Score: {total_score}")
            st.write(f"Sentiment: {sentiment}")

        sentiment_filter = st.selectbox(
            "Filter",
            ["All", "Positive", "Negative", "Neutral"]
        )

        min_score = st.slider("Min Score", -5, 5, -5)

        start_search = time.time()

        filtered = pd.DataFrame()

        if keyword.strip():
            filtered = results_df.copy()

            words = list(set(keyword.lower().split()))
            pattern = "|".join(map(re.escape, words))

            filtered = filtered[
                filtered["text"].str.lower().str.contains(pattern, regex=True)
            ]
        else:
            filtered = results_df.copy()   # ✅ IMPORTANT

        if sentiment_filter != "All":
            filtered = filtered[
                filtered["sentiment"] == sentiment_filter
            ]

        if "score" in filtered.columns:
           filtered = filtered[filtered["score"] >= min_score]
        
        end_search = time.time()

        st.info(f"🔍 Search Time: {round(end_search - start_search, 3)} sec")

        if keyword.strip():
            if filtered.empty:
                st.warning("No results found")
            else:
                st.dataframe(filtered)

        from database import insert_results

        if not filtered.empty and st.button("💾 Save Results"):
            st.session_state["saved_search"] = filtered

            # Save to DB
            insert_results(
               filtered[["id", "text", "score", "sentiment"]].values.tolist())
            
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