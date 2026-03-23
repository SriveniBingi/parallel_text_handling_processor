from multiprocessing import Pool
import os

# Import helper modules
from text_loader import chunk_data
from scorer import process_chunk
from database import create_table, insert_results


def run_processing(data, chunk_size):
    """
    Main function to handle parallel processing of text data.
    Steps:
    1. Validate data
    2. Split into chunks
    3. Process in parallel
    4. Flatten results
    5. Store in database
    """

    # ================= EDGE CASE =================
    # If no data → return empty list
    if not data:
        return []

    # ================= CHUNKING =================
    # Split data into smaller chunks for parallel processing
    chunks = list(chunk_data(data, chunk_size))

    # ================= PROCESS OPTIMIZATION =================
    # Use only required number of processes
    # Avoid creating more processes than chunks (waste of memory)
    num_processes = min(os.cpu_count(), len(chunks))

    # ================= PARALLEL PROCESSING =================
    # Each chunk is processed in parallel using multiple CPU cores
    with Pool(processes=num_processes) as pool:

        # map() distributes chunks across processes
        results = list(pool.imap_unordered(process_chunk, chunks))

        # OPTIONAL (FASTER for large data)
        # results = list(pool.imap_unordered(process_chunk, chunks))

    # ================= FLATTEN RESULTS =================
    # Convert list of lists → single list
    flat_results = [
        item
        for sublist in results
        for item in sublist
    ]

    # ================= DATABASE OPERATIONS =================
    # Create table if not exists
    #create_table()

    # Clear previous data (fresh run)
    #clear_table()

    # Insert new processed results
    #insert_results(flat_results)

    # ================= RETURN RESULTS =================
    return flat_results