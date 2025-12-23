from typing import List, Tuple
import requests


def geocode_address(address: str, api_key: str) -> Tuple[float, float]:
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    response = requests.get(
        url,
        params={"address": address, "key": api_key},
        timeout=30,
    ).json()

    status = response.get("status")
    if status != "OK":
        err_msg = response.get("error_message", "")
        raise ValueError(f"Geocode error for '{address}': status={status} message={err_msg}")

    loc = response["results"][0]["geometry"]["location"]
    return float(loc["lat"]), float(loc["lng"])


def distance_matrix_chunked(
    latlng_list: List[str],
    api_key: str,
    mode: str = "driving",
    max_elements: int = 100,
) -> dict:
    """
    Build full NxN Distance Matrix by splitting requests to avoid MAX_ELEMENTS_EXCEEDED.
    Elements = origins * destinations.

    For N points, we chunk origins into blocks so (block_size * N) <= max_elements.
    """
    n = len(latlng_list)
    if n == 0:
        raise ValueError("No locations provided for distance matrix.")

    block_size = max(1, max_elements // n)

    rows_all = []
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    for i in range(0, n, block_size):
        origins_block = latlng_list[i : i + block_size]

        response = requests.get(
            url,
            params={
                "origins": "|".join(origins_block),
                "destinations": "|".join(latlng_list),
                "mode": mode,
                "key": api_key,
            },
            timeout=60,
        ).json()

        status = response.get("status")
        if status != "OK":
            err_msg = response.get("error_message", "")
            raise ValueError(f"Distance Matrix error: status={status} message={err_msg}")

        rows_all.extend(response.get("rows", []))

    return {"status": "OK", "rows": rows_all}
