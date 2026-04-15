import pandas as pd
import numpy as np
import time


def load_points(path="cities.csv"):
    data = pd.read_csv(path, header=None, names=['x', 'y'])
    return data[['x', 'y']].values


def sum_squared_distances(centers, clusters):
    per_cluster = []
    total = 0.0
    for i, pts in enumerate(clusters):
        if len(pts) == 0:
            per_cluster.append(0.0)
            continue
        pts_arr = np.array(pts)
        s = np.sum((pts_arr - centers[i]) ** 2)
        per_cluster.append(float(s))
        total += s
    return total, per_cluster


def gradient_descent(points, k=3, learning_rate=0.01, iterations=100, seed=None, tol=1e-6):
    if seed is not None:
        np.random.seed(seed)
    centers = points[np.random.choice(len(points), k, replace=False)].astype(float)
    start = time.perf_counter()
    prev_total = None
    it_used = 0

    for it in range(iterations):
        it_used = it + 1
        clusters = [[] for _ in range(k)]
        for p in points:
            dists = [np.linalg.norm(p - c) for c in centers]
            idx = np.argmin(dists)
            clusters[idx].append(p)

        for i in range(k):
            if len(clusters[i]) > 0:
                grad = np.sum(centers[i] - np.array(clusters[i]), axis=0)
                centers[i] = centers[i] - learning_rate * 2 * grad

        total, _ = sum_squared_distances(centers, clusters)
        if prev_total is not None and abs(prev_total - total) < tol:
            break
        prev_total = total

    elapsed = time.perf_counter() - start
    total, per_cluster = sum_squared_distances(centers, clusters)
    return centers, clusters, total, per_cluster, it_used, elapsed


def newton_method(points, k=3, iterations=100, seed=None, tol=1e-6):
    if seed is not None:
        np.random.seed(seed)
    centers = points[np.random.choice(len(points), k, replace=False)].astype(float)
    start = time.perf_counter()
    it_used = 0
    for it in range(iterations):
        it_used = it + 1
        clusters = [[] for _ in range(k)]
        for p in points:
            dists = [np.linalg.norm(p - c) for c in centers]
            idx = np.argmin(dists)
            clusters[idx].append(p)

        new_centers = centers.copy()
        for i in range(k):
            if len(clusters[i]) > 0:
                new_centers[i] = np.mean(clusters[i], axis=0)
            else:
                new_centers[i] = points[np.random.choice(len(points))]

        if np.allclose(new_centers, centers, atol=tol, rtol=0):
            centers = new_centers
            break
        centers = new_centers

    elapsed = time.perf_counter() - start
    total, per_cluster = sum_squared_distances(centers, clusters)
    return centers, clusters, total, per_cluster, it_used, elapsed


def main():
    points = load_points("cities.csv")
    k = 3

    gd_centers, gd_clusters, gd_total, gd_per, gd_iters, gd_time = gradient_descent(points, k=k, learning_rate=0.01, iterations=1000, seed=42)
    nr_centers, nr_clusters, nr_total, nr_per, nr_iters, nr_time = newton_method(points, k=k, iterations=1000, seed=42)

    print("--- Gradient Descent ---")
    print("Centers:", gd_centers)
    print("Per-cluster SSD:", gd_per)
    print("Total SSD:", gd_total)
    print("Iterations used:", gd_iters, "Time (s):", round(gd_time, 6))
    print()
    print("--- Newton (K-means style) ---")
    print("Centers:", nr_centers)
    print("Per-cluster SSD:", nr_per)
    print("Total SSD:", nr_total)
    print("Iterations used:", nr_iters, "Time (s):", round(nr_time, 6))

    print()
    print("--- Comparison Summary ---")
    better = "Gradient Descent" if gd_total < nr_total else "Newton Method"
    print("Lower total SSD:", better)
    faster = "Gradient Descent" if gd_time < nr_time else "Newton Method"
    print("Faster (wall time):", faster)
    print("SSD difference (GD - Newton):", round(gd_total - nr_total, 6))


if __name__ == '__main__':
    main()