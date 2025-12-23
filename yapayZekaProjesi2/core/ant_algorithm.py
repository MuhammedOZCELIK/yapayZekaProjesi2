from typing import List, Tuple
import numpy as np


def _roulette_select(probabilities: np.ndarray, candidates: np.ndarray) -> int:
    r = np.random.rand()
    cum = 0.0
    for idx, p in zip(candidates, probabilities):
        cum += p
        if r <= cum:
            return int(idx)
    return int(candidates[-1])


def run_aco(
    cost: np.ndarray,
    ant_count: int,
    iteration_count: int,
    alpha: float,
    beta: float,
    evaporation_rate: float,
    pheromone_Q: float,
    start_index: int = 0,
) -> Tuple[List[int], float, List[float]]:
    """
    ACO for TSP-like tour:
    - visits all nodes once
    - returns to start
    Returns:
      best_path (includes return to start at the end),
      best_cost,
      best_cost_history (best so far per iteration)
    """
    n = cost.shape[0]
    if n < 2:
        raise ValueError("Cost matrix must have at least 2 nodes.")

    # Heuristic: eta = 1 / cost
    with np.errstate(divide="ignore", invalid="ignore"):
        eta = 1.0 / cost
        eta[~np.isfinite(eta)] = 0.0

    pheromone = np.ones((n, n), dtype=float) * 0.1

    best_path = None
    best_cost = float("inf")
    best_history: List[float] = []

    for _it in range(iteration_count):
        all_tours: List[Tuple[List[int], float]] = []

        for _k in range(ant_count):
            visited = [start_index]
            unvisited = set(range(n))
            unvisited.remove(start_index)

            tour_cost = 0.0
            current = start_index

            while unvisited:
                candidates = np.array(sorted(list(unvisited)), dtype=int)

                tau = pheromone[current, candidates] ** alpha
                he = eta[current, candidates] ** beta
                score = tau * he

                s = score.sum()
                if s <= 0:
                    # fallback: choose random among candidates
                    nxt = int(np.random.choice(candidates))
                else:
                    probs = score / s
                    nxt = _roulette_select(probs, candidates)

                tour_cost += cost[current, nxt]
                visited.append(nxt)
                unvisited.remove(nxt)
                current = nxt

            # return to start
            tour_cost += cost[current, start_index]
            visited.append(start_index)

            all_tours.append((visited, tour_cost))

            if tour_cost < best_cost:
                best_cost = tour_cost
                best_path = visited

        # Evaporation
        pheromone *= (1.0 - evaporation_rate)

        # Deposit pheromone
        for tour, tcost in all_tours:
            if not np.isfinite(tcost) or tcost <= 0:
                continue
            deposit = pheromone_Q / tcost
            for i in range(len(tour) - 1):
                a, b = tour[i], tour[i + 1]
                pheromone[a, b] += deposit
                pheromone[b, a] += deposit

        best_history.append(best_cost)

    if best_path is None:
        raise ValueError("ACO failed to find a valid tour.")

    return best_path, best_cost, best_history
