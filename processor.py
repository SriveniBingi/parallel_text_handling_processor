from multiprocessing import Pool
import os
from itertools import chain

# Import helper modules
from text_loader import chunk_data
from scorer import process_chunk

def run_processing(data, chunk_size):
    """
    Optimized for 1 Million+ rows using lazy evaluation and 
    memory-efficient flattening.
    """

    if not data:
        return []

    # 1. Use a Generator for chunking (saves RAM)
    # Don't convert to list() yet!
    chunks_generator = chunk_data(data, chunk_size)

    # 2. Dynamic Process Allocation
    num_processes = os.cpu_count()

    # 3. Parallel Processing with imap_unordered
    # chunksize in imap refers to how many chunks are sent to a worker at once
    processed_list = []
    
    with Pool(processes=num_processes) as pool:
        # imap_unordered is significantly faster and uses less memory
        # as it doesn't wait to preserve original order
        for result_chunk in pool.imap_unordered(process_chunk, chunks_generator):
            processed_list.append(result_chunk)

    # 4. Memory-Efficient Flattening
    # itertools.chain.from_iterable is much faster than list comprehension for 1M rows
    flat_results = list(chain.from_iterable(processed_list))

    # 5. Return for UI and Database
    return flat_results