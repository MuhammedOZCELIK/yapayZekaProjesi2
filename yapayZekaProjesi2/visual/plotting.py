
from typing import List, Tuple, Optional
import matplotlib.pyplot as plt


def plot_convergence(history: List[float], cost_type: str, save_path: Optional[str] = None):
    fig = plt.figure(figsize=(8, 5))
    plt.plot(history, marker="o")
    plt.title("ACO Convergence (Best Cost per Iteration)")
    plt.xlabel("Iteration")

    if cost_type == "duration":
        plt.ylabel("Best Duration (seconds)")
    else:
        plt.ylabel("Best Distance (meters)")

    plt.grid(True)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def plot_route(
    coords: List[Tuple[float, float]],
    path: List[int],
    labels: List[str],
    save_path: Optional[str] = None,
):
    fig = plt.figure(figsize=(9, 7))

    # plot points
    lats = [coords[i][0] for i in range(len(coords))]
    lngs = [coords[i][1] for i in range(len(coords))]
    plt.scatter(lngs, lats)

    # annotate
    for i, (lat, lng) in enumerate(coords):
        name = labels[i]
        # shorten label for plot
        short = name.split(",")[0][:30]
        plt.text(lng, lat, f"{i}: {short}", fontsize=8)

    # plot route lines
    for k in range(len(path) - 1):
        a = path[k]
        b = path[k + 1]
        plt.plot([coords[a][1], coords[b][1]], [coords[a][0], coords[b][0]])

    plt.title("Route Plot (Lat/Lng)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig
