from multiprocessing import Pool
import os
from text_loader import chunk_data
from scorer import process_chunk
from database import create_table, clear_table, insert_results


def run_processing(data, chunk_size):

    # Handle empty data
    if not data:
        return []

    # Create chunks
    chunks = list(chunk_data(data, chunk_size))

    # Optimize process count
    num_processes = min(os.cpu_count(), len(chunks))

    # Parallel processing
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_chunk, chunks)

    # Flatten results
    flat_results = [item for sublist in results for item in sublist]

    # Store in database
    create_table()
    clear_table()
    insert_results(flat_results)

    return flat_results