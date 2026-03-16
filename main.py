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
    search_by_name,
    search_by_sentiment,
    search_by_keyword,
    search_by_score
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


    # Step 5: Fetch All Records
    try:
        all_data = fetch_all()
        logging.info(f"Total records processed: {len(all_data)}")
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return


    # Step 6: Summary Report
    positive = sum(1 for row in all_data if row[4] == "Positive")
    negative = sum(1 for row in all_data if row[4] == "Negative")
    neutral = sum(1 for row in all_data if row[4] == "Neutral")

    print("\n===== Summary Report =====")
    print(f"Total Records : {len(all_data)}")
    print(f"Positive      : {positive}")
    print(f"Negative      : {negative}")
    print(f"Neutral       : {neutral}")


    # Step 7: Alert System for Negative Feedback
    print("\n⚠ Negative Feedback Alerts")

    alert_count = 0

    for row in all_data:
        if row[4] == "Negative":
            print(f"ALERT -> {row[1]} : {row[2]}")
            alert_count += 1

        if alert_count == 5:   # show only first 5 alerts
            break


    # Stop timer after processing (before user input)
    processing_end = time.time()

    logging.info(
        f"Processing completed in {round(processing_end - start_time, 2)} seconds."
    )


    # Step 8: Performance Report
    print("\n===== Performance Report =====")
    print(f"Dataset Size : {len(data)}")
    print(f"Chunks Created : {len(chunks)}")
    print(f"CPU Cores Used : {num_processes}")


    # Step 9: Search Options
    print("\nSearch Options")
    print("1 → Search by Student Name")
    print("2 → Search by Sentiment")
    print("3 → Search by Keyword")
    print("4 → Filter by Score")
    print("Press Enter to skip search")

    search_option = input("\nSelect option: ")


    try:

        # Search by Name
        if search_option == "1":

            name = input("Enter student name: ")
            results = search_by_name(name)
            if results:
                 print("\nSearch Results:\n")

                 for row in results:
                     print(row)

            else:
              print("No student found.")

            export_to_csv(results, "search_results.csv")
            logging.info("Search results exported to CSV.")
            


        # Search by Sentiment
        elif search_option == "2":

            sentiment = input("Enter sentiment (Positive/Negative/Neutral): ")
            results = search_by_sentiment(sentiment)

            for row in results:
                print(row)

            export_to_csv(results, "sentiment_results.csv")
            logging.info("Sentiment results exported to CSV.")


        # Search by Keyword
        elif search_option == "3":

            keyword = input("Enter keyword: ")
            results = search_by_keyword(keyword)

            for row in results:
                print(row)

            export_to_csv(results, "keyword_results.csv")
            logging.info("Keyword search results exported to CSV.")


        # Filter by Score
        elif search_option == "4":

            score = int(input("Enter maximum score (example: 0 or -1): "))
            results = search_by_score(score)

            for row in results:
                print(row)

            export_to_csv(results, "score_filtered_results.csv")
            logging.info("Score filtered results exported to CSV.")


        else:

            export_to_csv(all_data, "all_results.csv")
            logging.info("All results exported to CSV.")


    except Exception as e:
        logging.error(f"Search or CSV export error: {e}")


    logging.info("===== Program Finished Successfully =====")


if __name__ == "__main__":
    main()

