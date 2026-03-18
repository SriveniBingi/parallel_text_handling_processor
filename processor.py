from multiprocessing import Pool
import os
from text_loader import chunk_data
from scorer import process_chunk
from database import create_table, clear_table, insert_results


def run_processing(data):

    chunks = chunk_data(data)
    num_processes = os.cpu_count()

    with Pool(processes=num_processes) as pool:
        results = pool.map(process_chunk, chunks)

    flat_results = [item for sublist in results for item in sublist]

    create_table()
    clear_table()
    insert_results(flat_results)

    return flat_results