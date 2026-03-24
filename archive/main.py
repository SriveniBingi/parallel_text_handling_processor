import multiprocessing
from multiprocessing import Pool
import os
import time
import logging
import sys

# Importing your custom modules
from text_loader import read_csv, chunk_data
from config import DB_NAME, CHUNK_SIZE
from scorer import process_chunk
from database import (
    create_table,
    clear_table,
    insert_results,
    fetch_all,
    search_by_name,
    search_by_sentiment,
    search_by_keyword,
    search_by_score
)
from search_module import export_to_csv

# ================= LOGGING CONFIGURATION =================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("system_log.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    logging.info("===== ParaSense: CLI Engine Started =====")
    start_time = time.time()
    file_path = "data/students.csv"

    # --- STEP 1: DATA INGESTION ---
    try:
        data = read_csv(file_path)
        if not data:
            logging.warning("Dataset is empty. Exiting.")
            return
        logging.info(f"Total records loaded: {len(data)}")
    except Exception as e:
        logging.error(f"IO Error: {e}")
        return

    # --- STEP 2: CHUNKING STRATEGY ---
    try:
        # Using a balanced chunk size for 50k records
        chunks =list(chunk_data(data, CHUNK_SIZE)) 
        logging.info(f"Total chunks created: {len(chunks)}")
    except Exception as e:
        logging.error(f"Chunking Error: {e}")
        return

    # --- STEP 3: PARALLEL EXECUTION (MULTIPROCESSING) ---
    logging.info("Initiating Parallel Processing Pool...")
    try:
        num_processes = os.cpu_count()
        logging.info(f"Utilizing {num_processes} CPU cores")

        # The 'with' statement ensures resources are cleaned up automatically
        with Pool(processes=num_processes) as pool:
            # .map distributes the 'process_chunk' function across the pool
            results = pool.map(process_chunk, chunks)

    except Exception as e:
        logging.error(f"Multiprocessing Runtime Error: {e}")
        return

    # Flatten nested results from the pool
    flat_results = [item for sublist in results for item in sublist]

    # --- STEP 4: DATABASE PERSISTENCE ---
    try:
        create_table()
        clear_table() # Refreshing the database for the new run
        insert_results(flat_results)
        logging.info("Data successfully committed to SQLite.")
    except Exception as e:
        logging.error(f"Database Operational Error: {e}")
        return

    # --- STEP 5: ANALYTICAL REPORTING ---
    all_data = fetch_all()
    processing_end = time.time()
    
    positive = sum(1 for row in all_data if row[3] == "Positive")
    negative = sum(1 for row in all_data if row[3] == "Negative")
    neutral = sum(1 for row in all_data if row[3] == "Neutral")

    print("\n" + "="*30)
    print("📊 PARASENSE SUMMARY REPORT")
    print("="*30)
    print(f"Total Records   : {len(all_data)}")
    print(f"🟢 Positive     : {positive}")
    print(f"🔴 Negative     : {negative}")
    print(f"⚪ Neutral      : {neutral}")
    print(f"⚡ Time Elapsed  : {round(processing_end - start_time, 2)}s")
    print("="*30)

    # --- STEP 7: INTERACTIVE SEARCH & EXPORT ---
    print("\n🔎 POST-ANALYSIS SEARCH OPTIONS")
    print("1 → Search by Student Name")
    print("2 → Search by Sentiment")
    print("3 → Search by Keyword")
    print("4 → Filter by Score")
    print("Enter → Exit & Export All")

    option = input("\nSelect Option: ")

    try:
        search_results = []
        filename = "analysis_results.csv"

        if option == "1":
            name = input("Enter Student Name: ")
            search_results = search_by_name(name)
            filename = f"name_search_{name}.csv"
        elif option == "2":
            sent = input("Enter Sentiment (Positive/Negative/Neutral): ")
            search_results = search_by_sentiment(sent)
            filename = f"sentiment_{sent}.csv"
        elif option == "3":
            key = input("Enter Keyword: ")
            search_results = search_by_keyword(key)
            filename = f"keyword_{key}.csv"
        elif option == "4":
            score = int(input("Enter Min Score: "))
            search_results = search_by_score(score)
            filename = f"score_filter_{score}.csv"
        else:
            search_results = all_data
            filename = "all_processed_feedback.csv"

        if search_results:
            for row in search_results[:10]: # Preview top 10
                print(row)
            export_to_csv(search_results, filename)
            logging.info(f"Results exported to {filename}")
        else:
            print("No matching records found.")

    except Exception as e:
        logging.error(f"Search/Export Error: {e}")

    logging.info("===== ParaSense: Execution Cycle Finished =====")

if __name__ == "__main__":
    # Standard Windows Multiprocessing Protection
    main()