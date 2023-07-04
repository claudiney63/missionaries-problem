import Estado
from collections import deque

def bfs():
    """
     A função bfs() utiliza a busca em largura (BFS) para explorar todos os estados possíveis 
     até encontrar uma solução. Ela mantém uma fila de estados a serem explorados e uma lista de estados visitados 
     para evitar ciclos. A função retorna uma lista de ações que levam à solução, indicando quantos missionários e 
     canibais devem ser levados de uma margem para a outra em cada passo.
    """
    initial_state = Estado.Estado(3, 3, True)
    visited = set()
    queue = deque([(initial_state, [])])

    while queue:
        current_state, path = queue.popleft()
        if current_state.is_goal():
            return path

        visited.add(current_state)
        successors = current_state.successors()

        for successor, action in successors:
            if successor not in visited:
                queue.append((successor, path + [action]))

    return None

def dfs():
    """
    A função dfs() utiliza a busca em profundidade (DFS) para explorar os estados possíveis até encontrar uma solução. 
    Ela utiliza uma abordagem de "vá fundo" para explorar uma ramificação até o máximo possível antes de retroceder 
    e explorar outras ramificações.
    """
    initial_state = Estado.Estado(3, 3, True)
    visited = set()
    stack = [(initial_state, [])]

    while stack:
        current_state, path = stack.pop()
        if current_state.is_goal():
            return path

        visited.add(current_state)
        successors = current_state.successors()

        for successor, action in successors:
            if successor not in visited:
                stack.append((successor, path + [action]))

    return None

def show_resolution(typeSearch):
    solucao_bfs = typeSearch
    if solucao_bfs:
        lado = False
        for i, acao in enumerate(solucao_bfs):
            lado = not lado
            print(f"Passo {i+1}: Leve {acao[0]} missionarios e {acao[1]} canibais para o lado {'direito' if lado == True else 'esquerdo'}.")
    else:
        print("Não foi encontrada uma solução para o problema usando BFS.")


print("Busca em Largura (BFS):")
show_resolution(bfs())

print("\nBusca em Profundidade (DFS):")
show_resolution(dfs())
