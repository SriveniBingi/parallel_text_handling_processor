from multiprocessing import Pool
import os
from text_loader import chunk_data
from scorer import process_chunk
from database import create_table, clear_table, insert_results


def run_processing(data):
    """
    Main processing pipeline:
    - Chunk data
    - Run multiprocessing
    - Store results in DB
    - Return results
    """

    # Step 1: Chunk data
    chunks = chunk_data(data)

    # Step 2: Multiprocessing
    num_processes = os.cpu_count()

    with Pool(processes=num_processes) as pool:
        results = pool.map(process_chunk, chunks)

    # Step 3: Flatten results
    flat_results = [item for sublist in results for item in sublist]

    # Step 4: Store in DB
    create_table()
    clear_table()
    insert_results(flat_results)

    return flat_results