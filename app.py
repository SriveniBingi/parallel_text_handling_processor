import os
import json
import datetime
from collections import Counter

import pandas as pd
import streamlit as st
import plotly.express as px

from app.storage.storage import Storage
from app.search_export.search_save import search_in_storage
from app.text_processing.parallel_break_loader import pipeline_from_folder
from app.utils import get_env, ensure_dir

# ---------------- CONFIG ----------------
DB_PATH = get_env("DB_PATH", "checks.db")
TEXT_FOLDER = get_env("TEXT_FOLDER", "data/support_text_files")
RULES_PATH = get_env("RULES_PATH", "data/rules1.json")

ensure_dir(TEXT_FOLDER)
storage = Storage(DB_PATH)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Text Processor", layout="wide")

# ---------------- PREMIUM UI ----------------
st.markdown("""
<style>
body { background-color: #0e1117; }

.card {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

.section-title {
    font-size: 26px;
    font-weight: bold;
    margin-top: 20px;
}

.highlight {
    padding: 15px;
    border-radius: 10px;
    background-color: #111827;
    border-left: 5px solid #3b82f6;
    margin-bottom: 10px;
}

.alert-red {
    background-color: #2a0f0f;
    padding: 12px;
    border-radius: 10px;
    border-left: 5px solid red;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Parallel Text Intelligence System")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    rows = storage.query_checks(limit=10000)
    return pd.DataFrame(rows) if rows else pd.DataFrame()

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio("Navigation", [
    "Overview",
    "Upload Files",
    "Run Pipeline",
    "Search",
    "Analytics"
])

# ---------------- OVERVIEW ----------------
if menu == "Overview":
    df = load_data()

    st.markdown('<div class="section-title">📊 System Overview</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="highlight">
    1️⃣ Upload text files  
    2️⃣ Run pipeline  
    3️⃣ Search results  
    4️⃣ Analyze insights  
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f'<div class="card">📄 Total<br><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card">📊 Avg Score<br><h2>{round(df["score"].mean(),2) if not df.empty else 0}</h2></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card">🆔 Unique<br><h2>{df["uid"].nunique() if not df.empty else 0}</h2></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="card">⚠️ Alerts<br><h2>{len(df[df["score"]>70]) if not df.empty else 0}</h2></div>', unsafe_allow_html=True)

    # Alerts
    st.markdown('<div class="section-title">⚠️ Critical Alerts</div>', unsafe_allow_html=True)

    alerts = df[df["score"] > 70] if not df.empty else pd.DataFrame()

    if not alerts.empty:
        for _, row in alerts.head(5).iterrows():
            st.markdown(f"""
            <div class="alert-red">
            🚨 Score: {row['score']}<br>
            {row['text'][:150]}...
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No critical issues 🎉")

# ---------------- UPLOAD ----------------
elif menu == "Upload Files":
    st.header("📂 Upload Text Files")

    uploaded_files = st.file_uploader("Upload .txt files", accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            path = os.path.join(TEXT_FOLDER, file.name)
            with open(path, "wb") as f:
                f.write(file.getbuffer())
        st.success("Files uploaded successfully!")

# ---------------- PIPELINE ----------------
elif menu == "Run Pipeline":
    st.header("⚙️ Run Pipeline")

    workers = st.slider("Workers", 1, 16, 4)
    group_size = st.slider("Chunk Size", 100, 2000, 500)

    if st.button("🚀 Start Processing"):
        with st.spinner("Processing..."):
            progress = st.progress(0)

            for i in range(100):
                progress.progress(i + 1)

            results = pipeline_from_folder(
                folder_path=TEXT_FOLDER,
                rules_path=RULES_PATH,
                group_size=group_size,
                storage=storage,
                max_workers=workers,
                save=True
            )

        st.success(f"✅ Processed {len(results)} chunks")

# ---------------- SEARCH ----------------
elif menu == "Search":
    st.header("🔍 Smart Search")

    query = st.text_input("Enter keyword")
    df = load_data()

    if st.button("Search"):
        if query:
            results = search_in_storage(storage, query=query, limit=100)

            if results:
                df = pd.DataFrame(results)

                for _, row in df.head(10).iterrows():
                    color = "red" if row["score"] > 70 else "#22c55e"

                    st.markdown(f"""
                    <div class="highlight">
                    <b>Score:</b> <span style="color:{color}">{row['score']}</span><br>
                    {row['text'][:200]}...
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No results found")

# ---------------- ANALYTICS ----------------
elif menu == "Analytics":
    st.header("📊 Analytics Dashboard")

    df = load_data()

    if df.empty:
        st.warning("No data available")
    else:
        fig = px.histogram(df, x="score", nbins=40)
        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

        # Top rules
        st.subheader("Top Rule Hits")

        counter = Counter()
        for d in df["details"]:
            try:
                items = json.loads(d) if isinstance(d, str) else d
                for r in items:
                    counter[r.get("rule_id")] += 1
            except:
                pass

        if counter:
            rule_df = pd.DataFrame(counter.items(), columns=["Rule", "Hits"])
            fig2 = px.bar(rule_df.head(10), x="Rule", y="Hits")
            fig2.update_layout(template="plotly_dark")

            st.plotly_chart(fig2, use_container_width=True)