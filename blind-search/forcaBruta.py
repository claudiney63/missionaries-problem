import Estado
import psutil
import time
from collections import deque


def calcular_memoria_utilizada():
    processo = psutil.Process()
    memoria = processo.memory_info().rss
    return memoria / (1024 * 1024)  # Converter para megabytes


def bfs():
    nos_gerados = 0
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
                nos_gerados+=1

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
            print(
                f"Passo {i+1}: Leve {acao[0]} missionarios e {acao[1]} canibais para o lado {'direito' if lado == True else 'esquerdo'}.")
    else:
        print("Não foi encontrada uma solução para o problema usando BFS.")


print("Busca Força Bruta: ")
inicio = time.time()
memoria_inicial = calcular_memoria_utilizada()
print(f"Utilizacao de memoria antes: {memoria_inicial} MB")

print("Busca em Largura (BFS):")
show_resolution(bfs())

fim = time.time()
tempo_execucao = fim - inicio
memoria_final = calcular_memoria_utilizada()
print(f"Utilizacao de memoria depois: {memoria_final} MB")
diferenca_memoria = memoria_final - memoria_inicial
print(f"Diferenca de memoria: {diferenca_memoria} MB")
print(f"Tempo de execucao: {tempo_execucao} segundos")
busca ,nos_gerados = bfs()
print(f"Nós gerados: {nos_gerados}")
print("\nBusca em Profundidade (DFS):")
show_resolution(dfs())
