import time
from collections import deque
import Estado
import sys
import psutil

def calcular_memoria_utilizada():
    processo = psutil.Process()
    memoria = processo.memory_info().rss
    return memoria / (1024 * 1024)  # Converter para megabytes

def heuristic(state):
    return state.missionarios + state.canibais

def busca_gulosa():
    estado_inicial = Estado.Estado(3, 3, True)
    visitados = set()
    queue = deque([(estado_inicial, [])])
    nos_gerados = 1

    inicio = time.time()
    memoria_inicial = calcular_memoria_utilizada()
    print(f"Utilização de memória antes: {memoria_inicial} MB")

    while queue:
        queue = deque(sorted(queue, key=lambda x: heuristic(x[0])))
        estado_atual, caminho = queue.popleft()

        if estado_atual.is_goal():
            fim = time.time()
            tempo_execucao = fim - inicio

            memoria_final = calcular_memoria_utilizada()
            print(f"Utilização de memória depois: {memoria_final} MB")

            diferenca_memoria = memoria_final - memoria_inicial
            print(f"Diferença de memória: {diferenca_memoria} MB")
            print(f"Tempo de execução: {tempo_execucao} segundos")

            return caminho

        visitados.add(estado_atual)
        sucessores = estado_atual.successors()

        for sucessor, acao in sucessores:
            if sucessor not in visitados:
                queue.append((sucessor, caminho + [acao]))
                nos_gerados += 1

    fim = time.time()
    tempo_execucao = fim - inicio

    memoria_final = calcular_memoria_utilizada()
    print(f"Utilização de memória depois: {memoria_final} MB")

    diferenca_memoria = memoria_final - memoria_inicial
    print(f"Diferença de memória: {diferenca_memoria} MB")
    print(f"Tempo de execução: {tempo_execucao} segundos")

    return None

print("Busca Gulosa:")
solucao_gulosa = busca_gulosa()
if solucao_gulosa:
    lado = False
    for i, acao in enumerate(solucao_gulosa):
        lado = not lado
        print(f"Passo {i+1}: Leve {acao[0]} missionários e {acao[1]} canibais para o lado {'direito' if lado == True else 'esquerdo'}.")
else:
    print("Não foi encontrada uma solução para o problema usando busca gulosa.")
