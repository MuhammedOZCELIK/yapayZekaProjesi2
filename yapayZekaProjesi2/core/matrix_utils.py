from typing import Literal
import numpy as np


def build_cost_matrix(dm_json: dict, cost_type: Literal["duration", "distance"]) -> np.ndarray:
    """
    Convert Google Distance Matrix JSON into NxN cost matrix.
    - duration: seconds
    - distance: meters
    Diagonal is set to infinity.
    """
    rows = dm_json.get("rows", [])
    n = len(rows)
    if n == 0:
        raise ValueError("Distance Matrix JSON has no rows.")

    matrix = np.zeros((n, n), dtype=float)

    for i in range(n):
        elements = rows[i].get("elements", [])
        if len(elements) != n:
            raise ValueError("Distance Matrix row has unexpected number of elements.")
        for j in range(n):
            el = elements[j]
            status = el.get("status", "OK")
            if i == j:
                matrix[i, j] = float("inf")
                continue
            if status != "OK":
                matrix[i, j] = float("inf")
                continue

            if cost_type == "duration":
                matrix[i, j] = float(el["duration"]["value"])
            else:
                matrix[i, j] = float(el["distance"]["value"])

    return matrix
