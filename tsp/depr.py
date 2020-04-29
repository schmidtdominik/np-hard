def populate_nn_basic(global_pool, points, distance_matrix, timeout=1.0):
    print('NN POP')
    t0 = time.time()
    step = 0
    while time.time() - t0 < timeout:
        visited = np.zeros((len(points)), dtype=np.bool)
        sol = []

        init = random.randint(0, len(points) - 1)
        visited[init] = True
        sol.append(init)

        for i in range(len(points) - 1):
            legal_indices = np.nonzero(np.invert(visited))[0]
            distances = distance_matrix[sol[-1]][legal_indices]
            selected_legal = np.argmin(distances)
            sel = legal_indices[selected_legal]
            visited[sel] = True
            sol.append(sel)
        global_pool.push(sol, cost(sol, distance_matrix))
        step += 1
        # global_pool.print_stats()
    return step, time.time()-t0