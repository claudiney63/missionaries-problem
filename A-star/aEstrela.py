from collections import deque
import Estado

def heuristic(state):
    # Função heurística: número de missionários e canibais ainda na margem esquerda
    return state.missionarios + state.canibais

def a_star_search():
    initial_state = Estado.Estado(3, 3, True)
    visited = set()
    queue = deque([(initial_state, [])])

    while queue:
        queue = deque(sorted(queue, key=lambda x: len(x[1]) + heuristic(x[0])))  # Ordena a fila com base na função heurística e no custo do caminho
        current_state, path = queue.popleft()
        if current_state.is_goal():
            return path

        visited.add(current_state)
        successors = current_state.successors()

        for successor, action in successors:
            if successor not in visited:
                queue.append((successor, path + [action]))

    return None

print("A* Search:")
solucao_astar = a_star_search()
if solucao_astar:
    lado = False
    for i, acao in enumerate(solucao_astar):
        lado = not lado
        print(f"Passo {i+1}: Leve {acao[0]} missionarios e {acao[1]} canibais para o lado {'direito' if lado == True else 'esquerdo'}.")
else:
    print("Não foi encontrada uma solução para o problema usando A* Search.")
