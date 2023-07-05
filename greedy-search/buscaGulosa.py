from collections import deque
import Estado 

def heuristic(state):
    # Função heurística: número de missionários e canibais ainda na margem esquerda
    return state.missionarios + state.canibais

def greedy_search():
    initial_state = Estado.Estado(3, 3, True)
    visited = set()
    queue = deque([(initial_state, [])])

    while queue:
        queue = deque(sorted(queue, key=lambda x: heuristic(x[0])))  # Ordena a fila com base na heurística
        current_state, path = queue.popleft()
        if current_state.is_goal():
            return path

        visited.add(current_state)
        successors = current_state.successors()

        for successor, action in successors:
            if successor not in visited:
                queue.append((successor, path + [action]))

    return None

print("Busca Gulosa:")
solucao_gulosa = greedy_search()
if solucao_gulosa:
    lado = False
    for i, acao in enumerate(solucao_gulosa):
        lado = not lado
        print(f"Passo {i+1}: Leve {acao[0]} missionarios e {acao[1]} canibais para o lado {'direito' if lado == True else 'esquerdo'}.")
else:
    print("Não foi encontrada uma solução para o problema usando busca gulosa.")
