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
    nodes_expanded = 0
    nodes_frontier = 0

    while queue:
        current_state, path = queue.popleft()
        nodes_frontier -= 1
        nodes_expanded += 1

        if current_state.is_goal():
            return path, nodes_expanded, nodes_frontier

        visited.add(current_state)
        successors = current_state.successors()

        for successor, action in successors:
            if successor not in visited:
                queue.append((successor, path + [action]))
                visited.add(successor)
                nodes_frontier += 1

    return None, nodes_expanded, nodes_frontier

def dfs():
    """
    A função dfs() utiliza a busca em profundidade (DFS) para explorar os estados possíveis até encontrar uma solução. 
    Ela utiliza uma abordagem de "vá fundo" para explorar uma ramificação até o máximo possível antes de retroceder 
    e explorar outras ramificações.
    """
    initial_state = Estado.Estado(3, 3, True)
    visited = set()
    stack = [(initial_state, [])]
    nodes_expanded = 0
    nodes_frontier = 0

    while stack:
        current_state, path = stack.pop()
        nodes_expanded += 1

        if current_state.is_goal():
            return path, nodes_expanded, nodes_frontier

        visited.add(current_state)
        successors = current_state.successors()

        for successor, action in successors:
            if successor not in visited:
                stack.append((successor, path + [action]))
                visited.add(successor)
                nodes_frontier += 1

    return None, nodes_expanded, nodes_frontier

def show_resolution(typeSearch):
    solucao, nos_expandidos, nos_fronteira = typeSearch
    if solucao:
        lado = False
        for i, acao in enumerate(solucao):
            lado = not lado
            print(f"Passo {i+1}: Leve {acao[0]} missionários e {acao[1]} canibais para o lado {'direito' if lado == True else 'esquerdo'}.")
    else:
        print("Não foi encontrada uma solução para o problema.")

    print("Número de nós expandidos:", nos_expandidos)
    print("Número de nós na fronteira:", nos_fronteira)


print("Busca em Largura (BFS):")
show_resolution(bfs())

print("\nBusca em Profundidade (DFS):")
show_resolution(dfs())
