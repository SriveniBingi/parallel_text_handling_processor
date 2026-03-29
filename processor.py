from multiprocessing import Pool
import os

# Import helper modules
from text_loader import chunk_data
from scorer import process_chunk


def run_processing(data, chunk_size):
    """
    Main processing pipeline:
    1. Split data into chunks (memory efficient)
    2. Process chunks in parallel using multiprocessing
    3. Merge results efficiently

    Designed for handling large datasets (1M+ rows)
    """

    # Safety check: return empty list if no data
    if not data:
        return []

    # --------------------------------------------------
    # STEP 1: Chunking (Generator-based)
    # --------------------------------------------------
    # chunk_data returns a generator → saves RAM
    # Instead of loading all chunks into memory at once
    chunks_generator = chunk_data(data, chunk_size)

    # --------------------------------------------------
    # STEP 2: Dynamic CPU Core Allocation
    # --------------------------------------------------
    # Automatically uses all available CPU cores
    num_processes = os.cpu_count()

    # --------------------------------------------------
    # STEP 3: Parallel Processing
    # --------------------------------------------------
    # We use imap_unordered for:
    # ✔ Faster execution
    # ✔ Non-blocking results
    # ✔ Lower memory usage
    # Order of results is not guaranteed (acceptable here)

    flat_results = []  # Final merged results

    with Pool(processes=num_processes) as pool:
        for result_chunk in pool.imap_unordered(process_chunk, chunks_generator):
            
            # --------------------------------------------------
            # STEP 4: Efficient Merging
            # --------------------------------------------------
            # Instead of storing all chunks first (high memory),
            # we directly extend the final list
            flat_results.extend(result_chunk)

    # --------------------------------------------------
    # STEP 5: Return Final Results
    # --------------------------------------------------
    # Ready for UI display and database storage
    return flat_results