from multiprocessing import Pool
import os
import time
import logging
from text_loader import read_csv, chunk_data
from scorer import process_chunk
from database import (
    create_table,
    clear_table,
    insert_results,
    fetch_all,
    search_by_name
)
from search_module import export_to_csv

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    logging.info("===== Student Feedback Processing System Started =====")
    
    start_time = time.time()

    file_path = "data/students.csv"

    # Step 1: Read CSV
    try:
        data = read_csv(file_path)
        logging.info(f"Total records loaded: {len(data)}")
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        return

    # Step 2: Chunk Data
    try:
        chunks = chunk_data(data)
        logging.info(f"Total chunks created: {len(chunks)}")
    except Exception as e:
        logging.error(f"Error during chunking: {e}")
        return



    # Step 3: Parallel Processing
    logging.info("Processing feedback in parallel...")

    try:
        num_processes = os.cpu_count()
        logging.info(f"Using {num_processes} CPU cores for multiprocessing")

        with Pool(processes=num_processes) as pool:
            results = pool.map(process_chunk, chunks)

    except Exception as e:
        logging.error(f"Multiprocessing error: {e}")
        return

    # Flatten results
    flat_results = [item for sublist in results for item in sublist]


    # Step 4: Store in Database
    try:
        create_table()
        clear_table()
        insert_results(flat_results)
        logging.info("Data stored in database successfully.")
    except Exception as e:
        logging.error(f"Database error: {e}")
        return
    
    

    # Step 5: Show total records
    try:
        all_data = fetch_all()
        logging.info(f"Total records processed: {len(all_data)}")
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return
    
    # Stop timer after processing (before user input)
    processing_end = time.time()
    logging.info(f"Processing completed in {round(processing_end - start_time, 2)} seconds.")


    # Step 6: Search Option
    search_name = input("\nEnter student name to search (or press Enter to skip): ")

    try:
        if search_name:
            search_results = search_by_name(search_name)

            for row in search_results:
                print(row)

            export_to_csv(search_results, "search_results.csv")
            logging.info("Search results exported to CSV.")

        else:
            export_to_csv(all_data)
            logging.info("All data exported to CSV.")

    except Exception as e:
        logging.error(f"CSV export error: {e}")

    logging.info("===== Program Finished Successfully =====")

if __name__ == "__main__":
    main()