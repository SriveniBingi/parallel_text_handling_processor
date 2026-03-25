# 🚀 ParaSense: Parallel Text Handling & Sentiment Engine

A high-performance, scalable, multi-core **Text Processing, Rule-Based Scoring, and Relational Analytics System** built entirely in Python.

This project is specifically designed for **fast batch processing**, **parallel text chunking**, and **rule-based compliance scoring**—all **optimized for large-scale text workflows** 

---

## 📌 Features at a Glance

* ⚡ **Parallel Text Chunking** — Utilizes `multiprocessing.Pool` for concurrent execution.
* 📚 **Rule-Based Sentiment Engine** — High-speed Regex-based scoring heuristics.
* 🧠 **Advanced Logic** — Handles Negations (*not, never*) and Intensifiers (*very, highly*).
* 🗃️ **SQLite Persistence** — Relational storage with indexed sub-second searching.
* 🔍 **Power Search Interface** — Multi-parameter filtering (Name, Keyword, Sentiment).
* 📊 **Interactive Analytics Dashboard** — Built with Streamlit for real-time visualization.
* 🛠 **N-Tier Architecture** — Fully decoupled, modular design for maximum maintainability.

---

## 🏗️ System Architecture

ParaSense follows a modular data pipeline, ensuring a clear separation between data ingestion, analytical logic, and the presentation layer.

```text
       [ INPUT ]              [ PROCESSING ]             [ OUTPUT ]
    +--------------+       +------------------+       +--------------+
    | students.csv | ----> |  text_loader.py  | ----> |   app.py     |
    | (50k Records)|       | (Chunking Logic) |       | (Streamlit)  |
    +--------------+       +--------+---------+       +--------------+
                                    |
                                    v
                           +------------------+       +--------------+
                           |   processor.py   | ----> |   main.py    |
                           | (Multiprocessing)|       |    (CLI)     |
                           +--------+---------+       +--------------+
                                    |
            +-----------------------+-----------------------+
            |                       |                       |
            v                       v                       v
    +--------------+       +------------------+       +--------------+
    |  scorer.py   | <---> |   database.py    | <---> | analysis.db  |
    | (Regex Logic)|       |  (SQL Engine)    |       | (Persistence)|
    +--------------+       +------------------+       +--------------+
```
---
## 📂 Project Folder Structure
```
parallel_text_handling_processor/
│
├── data/                       # 📁 Data Layer (CSV Input)
│   └── students.csv
│
├── scripts/                    # 🛠️ Utility Layer
│   └── generate_students.py    # Dataset generator
│
├── archive/                    # 📦 History Layer
│   ├── cli_version.py          # Legacy Milestone 1/2 files
│   └── search_module.py
│
├── config.py                   # ⚙️ Global Settings (Lexicons, DB Name)
├── database.py                 # 🗄️ Persistence Layer (SQL Logic)
├── scorer.py                   # 🧠 Analytical Layer (Regex Scoring)
├── processor.py                # 🚀 Execution Engine (Multiprocessing)
├── text_loader.py              # 📥 Ingestion Layer (Chunking)
├── app.py                      # 🎨 Presentation Layer (Streamlit UI)
├── main.py                     # 💻 Presentation Layer (CLI Engine)
│
├── requirements.txt            # 📋 Dependencies
├── README.md                   # 📖 Project Documentation
└── Agile_Log.md                # 📝 Milestone Tracking
```

---
## ⚙️ System Workflow (The Pipeline)

The application operates as a linear, automated pipeline to ensure maximum data integrity and processing speed:

| Step | Phase          | Action                                                                        |
| :--- | :------------- | :---------------------------------------------------------------------------- |
| **1** | **Ingestion** | `text_loader.py` streams the raw CSV and divides data into 1,000-row chunks. |
| **2** | **Distribution** | `processor.py` initializes a `multiprocessing.Pool` to assign chunks to cores. |
| **3** | **Analysis** | `scorer.py` applies Regex heuristics to calculate sentiment scores per record. |
| **4** | **Persistence** | `database.py` performs atomic batch inserts into the SQLite database.         |

## 🖥️ Interfaces

### 1. Streamlit Dashboard
**Run:** `streamlit run app.py`

* **Real-time Metrics:** View processing time and core utilization.
* **Visual Analytics:** Interactive Pie charts and Bar graphs of sentiment distribution.
* **Data Browser:** Filter and search through processed records instantly.

### 2. High-Performance CLI
**Run:** `python main.py`

   * Designed for server-side processing and quick administrative searches.

---
## 🧩 Module Breakdown

| Module | Responsibility |
| :--- | :--- |
| **`app.py`** | **Presentation Layer:** The interactive Streamlit dashboard for visual data mining. |
| **`processor.py`** | **Execution Layer:** Manages parallel worker processes and cross-core communication. |
| **`scorer.py`** | **Analytical Layer:** Contains the Regex "Brain" for sentiment and negation logic. |
| **`database.py`** | **Persistence Layer:** Handles all SQL operations, table indexing, and search queries. |
| **`text_loader.py`** | **Ingestion Layer:** Efficiently streams large files without consuming excess RAM. |
| **`config.py`** | **Configuration Layer:** Centralized storage for lexicons, file paths, and settings. |
---

## 🧱 Tech Stack

| Category         | Technology               | Purpose                                     |
| ---------------- | ------------------------ | ------------------------------------------- |
| Language         | Python 3.11+             | Core application logic and processing.      |
| Parallelism      | Multiprocessing          | Concurrent execution across CPU cores.      |
| Data Handling    | Pandas                   | Efficient CSV ingestion and cleaning.       |
| Persistence      | SQLite 3                 | Indexed relational storage for fast search. |
| Web UI           | Streamlit                | Interactive dashboard and visualization.    |
| Analytics        | Plotly / Matplotlib      | Sentiment and performance charts.           |
| Logic Engine     | Regex (re)               | Sentiment heuristics (Negation handling).   |
| Logging          | Python Logging           | System monitoring and error tracking.       |

---

## **⚙️ Installation & Setup**
1. Clone the repo
   
   ```
   git clone https://github.com/SriveniBingi/parallel_text_handling_processor.git
   cd parallel_text_handling_processor
   ```
3. Install Dependencies
   
   ```
   pip install -r requirements.txt
   ```
5. Run the Pipeline
   
   ```
   python main.py
   ```
---

## 🗺️ Milestone Roadmap

| Milestone     | Status | Description                                                    |
| ------------- | ------ | ---------------------------------------------------------------|
| M1:Setup      | ✅     | Environment setup, Database schema, and Regex Lexicon.         |
| M2:Loader     | ✅     | Built parallel chuncking; tested with 5000 records             |
| M3:Scorer     | ✅     | Integrated SQLite & Regex Engine; scaled to 50k records        |
| M4:Launch     | 🚀     | Streamlit Dashboard & Final Optimization, Documentation Launch.|

---
### **👥 Author**

* Sriveni Bingi
* MCA Student 
