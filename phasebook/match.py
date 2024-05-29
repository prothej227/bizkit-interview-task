import time
from flask import Blueprint
from concurrent.futures import ThreadPoolExecutor, as_completed
from more_itertools import chunked
from .data.match_data import MATCHES
from typing import Dict, List, Any

bp = Blueprint("match", __name__, url_prefix="/match")

@bp.route("<int:match_id>")
def match(match_id):
    if match_id < 0 or match_id >= len(MATCHES):
        return "Invalid match id", 404

    start = time.time()
    msg = "Match found" if (is_match(*MATCHES[match_id])) else "No match"
    end = time.time()

    return {"message": msg, "elapsedTime": end - start}, 200


def is_match(fave_numbers_1 : List, fave_numbers_2: List) -> bool:

    # Set per batch processing, where batch_size = 10k
    batch_size = 10000
    fave_numbers_set = set(fave_numbers_1)

    # Compute number of workers from batch/chunk size
    num_workers = max(1, len(fave_numbers_2) // batch_size)
    batches = chunked(fave_numbers_2, batch_size)

    def check_subset(subset):
        return all(num in fave_numbers_set for num in subset)

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(check_subset, batch) for batch in batches]

        for future in as_completed(futures):
            # Check for falsy result: if false detected, return False
            if not future.result():
                return False
            
    return True

    