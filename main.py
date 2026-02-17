from multiprocessing import Pool
import time
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


def main():
    print("\n===== Student Feedback Processing System =====\n")

    start_time = time.time()

    file_path = "data/students.csv"

    # Step 1: Read CSV
    data = read_csv(file_path)

    # Step 2: Chunk Data
    chunks = chunk_data(data)

    # Step 3: Parallel Processing
    print("Processing feedback in parallel...\n")

    with Pool() as pool:
        results = pool.map(process_chunk, chunks)

    flat_results = [item for sublist in results for item in sublist]

    # Step 4: Store in Database
    create_table()
    clear_table()
    insert_results(flat_results)

    print("Data stored in database successfully.\n")

    # Step 5: Show total records
    all_data = fetch_all()
    print(f"Total records processed: {len(all_data)}")

    # Step 6: Search Option
    search_name = input("\nEnter student name to search (or press Enter to skip): ")

    if search_name:
        search_results = search_by_name(search_name)
        for row in search_results:
            print(row)
        export_to_csv(search_results, "search_results.csv")
    else:
        export_to_csv(all_data)

    end_time = time.time()

    print(f"\nProcessing completed in {round(end_time - start_time, 2)} seconds.")
    print("\n==============================================\n")


if __name__ == "__main__":
    main()
