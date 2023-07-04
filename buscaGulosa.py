from Estado import *
import time
from collections import deque
import sys
import psutil


def calcular_memoria_utilizada():
    processo = psutil.Process()
    memoria = processo.memory_info().rss
    return memoria / (1024 * 1024)  # Converter para megabytes

def heuristic(state):
    return state.missionarios + state.canibais

def busca_gulosa():
    estado_inicial = Estado(3, 3, True)
    visitados = set()
    queue = deque([(estado_inicial, [])])
    nos_gerados = 1
    nos_fronteira = 1
    nos_expandidos = 0

    inicio = time.time()
    memoria_inicial = calcular_memoria_utilizada()
    print(f"Utilização de memória antes: {memoria_inicial} MB")

    while queue:
        queue = deque(sorted(queue, key=lambda x: heuristic(x[0])))
        estado_atual, caminho = queue.popleft()
        nos_fronteira -= 1
        nos_expandidos += 1

        if estado_atual.is_goal():
            fim = time.time()
            tempo_execucao = fim - inicio

            memoria_final = calcular_memoria_utilizada()
            print(f"Utilização de memória depois: {memoria_final} MB")

            diferenca_memoria = memoria_final - memoria_inicial
            print(f"Diferença de memória: {diferenca_memoria} MB")
            print(f"Tempo de execução: {tempo_execucao} segundos")

            return caminho, nos_gerados, nos_fronteira, nos_expandidos

        visitados.add(estado_atual)
        sucessores = estado_atual.successors()

        print("Estado atual: ", estado_atual)
        for sucessor, acao in sucessores:
            new_state = Estado(sucessor.missionarios, sucessor.canibais, sucessor.barco_esquerda)
            valid_indicator = "(V)" if new_state.is_valid() else "(X)"
            visited_indicator = "(R)" if str(new_state) in visitados else "( )"
            print(f"  Ação: {acao}, Sucessor: {new_state} {valid_indicator} {visited_indicator}")

            if new_state not in visitados:
                queue.append((new_state, caminho + [acao]))
                nos_gerados += 1
                nos_fronteira += 1

    fim = time.time()
    tempo_execucao = fim - inicio

    memoria_final = calcular_memoria_utilizada()
    print(f"Utilização de memória depois: {memoria_final} MB")

    diferenca_memoria = memoria_final - memoria_inicial
    print(f"Diferença de memória: {diferenca_memoria} MB")
    print(f"Tempo de execução: {tempo_execucao} segundos")

    return None, nos_gerados, nos_fronteira, nos_expandidos

print("Busca Gulosa:")
solucao_gulosa, nos_gerados, nos_fronteira, nos_expandidos = busca_gulosa()
if solucao_gulosa:
    lado = False
    for i, acao in enumerate(solucao_gulosa):
        lado = not lado
        print(f"Passo {i+1}: Leve {acao[0]} missionários e {acao[1]} canibais para o lado {'direito' if lado == True else 'esquerdo'}.")
else:
    print("Não foi encontrada uma solução para o problema usando busca gulosa.")

print(f"Quantidade de nós gerados: {nos_gerados}")
print(f"Quantidade de nós de fronteira: {nos_fronteira}")
print(f"Quantidade de nós expandidos: {nos_expandidos}")
