from collections import deque

class Estado:
    def __init__(self, missionarios, canibais, barco_esquerda):
        self.missionarios = missionarios
        self.canibais = canibais
        self.barco_esquerda = barco_esquerda

    def is_valid(self):
        if self.missionarios < 0 or self.canibais < 0 or self.missionarios > 3 or self.canibais > 3:
            return False
        if self.missionarios > 0 and self.missionarios < self.canibais:
            return False
        if self.missionarios < 3 and (3 - self.missionarios) < (3 - self.canibais):
            return False
        return True

    def is_goal(self):
        return self.missionarios == 0 and self.canibais == 0 and not self.barco_esquerda

    def successors(self):
        successors = []
        if self.barco_esquerda:
            for m in range(1, self.missionarios + 1):
                for c in range(1, self.canibais + 1):
                    if m + c <= 2:
                        new_state = Estado(self.missionarios - m, self.canibais - c, not self.barco_esquerda)
                        if new_state.is_valid():
                            successors.append((new_state, (m, c)))
        else:
            for m in range(1, 4 - self.missionarios + 1):
                for c in range(1, 4 - self.canibais + 1):
                    if m + c <= 2:
                        new_state = Estado(self.missionarios + m, self.canibais + c, not self.barco_esquerda)
                        if new_state.is_valid():
                            successors.append((new_state, (m, c)))
        return successors

def heuristic(state):
    # Função heurística: número de missionários e canibais ainda na margem esquerda
    return state.missionarios + state.canibais

def a_star_search():
    initial_state = Estado(3, 3, True)
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
    for i, acao in enumerate(solucao_astar):
        print(f"Passo {i+1}: Leve {acao[0]} missionários e {acao[1]} canibais para o outro lado.")
else:
    print("Não foi encontrada uma solução para o problema usando A* Search.")
