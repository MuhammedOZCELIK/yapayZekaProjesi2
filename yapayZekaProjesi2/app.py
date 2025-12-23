import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from core.google_maps import geocode_address, distance_matrix_chunked
from core.matrix_utils import build_distance_matrix
from core.ant_algorithm import run_aco
from config import ACO_CONFIG


st.set_page_config(page_title="Scenario 3 - ACO Route Optimization", layout="wide")
st.title("Scenario 3 - Ant Colony Optimization with Google Maps")

api_key = st.secrets.get("GOOGLE_MAPS_API_KEY", "")

# Initialize session state keys
if "result" not in st.session_state:
    st.session_state["result"] = None
if "error" not in st.session_state:
    st.session_state["error"] = None

with st.sidebar:
    st.subheader("Inputs")

    depot = st.text_input("Depot address", "Bursa, Turkey")

    schools_text = st.text_area(
        "12 school addresses (one per line)",
        height=260,
    )

    cost_type = st.selectbox("Cost type", ["duration", "distance"], index=0)

    col_a, col_b = st.columns(2)
    with col_a:
        run = st.button("Run ACO", disabled=not api_key, use_container_width=True)
    with col_b:
        clear = st.button("Clear Results", use_container_width=True)

if clear:
    st.session_state["result"] = None
    st.session_state["error"] = None
    st.rerun()

# Run ACO only when button clicked
if run:
    st.session_state["error"] = None

    schools = [s.strip() for s in schools_text.splitlines() if s.strip()]
    if len(schools) != 12:
        st.session_state["error"] = "Exactly 12 school addresses are required (one per line)."
        st.session_state["result"] = None
        st.rerun()

    addresses = [depot] + schools  # 0 depot, 1..12 schools

    # Geocode
    coords = []
    bad_addresses = []
    for addr in addresses:
        try:
            coords.append(geocode_address(addr, api_key))
        except Exception as e:
            bad_addresses.append((addr, str(e)))

    if bad_addresses:
        st.session_state["error"] = f"Some addresses could not be geocoded: {bad_addresses}"
        st.session_state["result"] = None
        st.rerun()

    # Chunked Distance Matrix
    latlng = [f"{lat},{lng}" for (lat, lng) in coords]
    dm = distance_matrix_chunked(latlng, api_key, max_elements=100)

    # Matrix for ACO
    dist = build_distance_matrix(dm, cost_type)

    # Run ACO
    best_path, best_cost, history = run_aco(
        dist,
        ant_count=ACO_CONFIG["ant_count"],
        iteration_count=ACO_CONFIG["iteration_count"],
        alpha=ACO_CONFIG["alpha"],
        beta=ACO_CONFIG["beta"],
        evaporation_rate=ACO_CONFIG["evaporation_rate"],
        pheromone_Q=ACO_CONFIG["pheromone_Q"],
    )

    # Save results in session state
    st.session_state["result"] = {
        "addresses": addresses,
        "coords": coords,
        "best_path": best_path,
        "best_cost": best_cost,
        "history": history,
        "cost_type": cost_type,
    }
    st.rerun()

# Show any error message
if st.session_state["error"]:
    st.error(st.session_state["error"])

# Display results if available
res = st.session_state["result"]
if res:
    addresses = res["addresses"]
    coords = res["coords"]
    best_path = res["best_path"]
    best_cost = res["best_cost"]
    cost_type = res["cost_type"]

    df = pd.DataFrame(
        {
            "Order": list(range(len(best_path))),
            "NodeIndex": best_path,
            "Address": [addresses[i] for i in best_path],
        }
    )

    st.success("Route calculated successfully.")

    st.subheader("Route Table")
    st.dataframe(df, use_container_width=True)

    st.subheader("Total Cost")
    if cost_type == "duration":
        st.write(f"Total duration: {best_cost / 60:.1f} minutes")
    else:
        st.write(f"Total distance: {best_cost / 1000:.2f} km")

    st.subheader("Visit Order")
    st.write(" -> ".join([addresses[i] for i in best_path]))

    st.subheader("Route on Map")
    depot_lat, depot_lng = coords[0]
    m = folium.Map(location=[depot_lat, depot_lng], zoom_start=11)

    folium.Marker(
        [depot_lat, depot_lng],
        popup=f"Depot: {addresses[0]}",
        tooltip="Depot",
        icon=folium.Icon(color="green"),
    ).add_to(m)

    for idx in range(1, len(addresses)):
        lat, lng = coords[idx]
        folium.Marker(
            [lat, lng],
            popup=f"{idx}. {addresses[idx]}",
            tooltip=f"Stop {idx}",
            icon=folium.Icon(color="blue"),
        ).add_to(m)

    route_points = [coords[i] for i in best_path]
    folium.PolyLine(route_points, weight=5).add_to(m)

    st_folium(m, width=1200, height=650)
else:
    if not api_key:
        st.warning("Missing GOOGLE_MAPS_API_KEY in .streamlit/secrets.toml")
    else:
        st.info("Enter 12 addresses and click 'Run ACO'.")
