# import networkx as nx
# import matplotlib.pyplot as plt
from collections import deque
import Estado

def heuristica(estado):
    # Função heurística: número de missionários e canibais ainda na margem esquerda
    return estado.missionarios + estado.canibais

def busca_a_estrela():
    esatdo_inicial = Estado.Estado(3, 3, True)  # Cria um estado inicial com 3 missionários e 3 canibais na margem esquerda
    visitados = set()  # Conjunto para armazenar os estados visitados
    queue = deque([(esatdo_inicial, [])])  # Fila para armazenar os estados a serem explorados, com o estado inicial e um caminho vazio
    caminhos = []  # Lista para armazenar os caminhos percorridos em cada iteração

    while queue:
        queue = deque(sorted(queue, key=lambda x: len(x[1]) + heuristica(x[0])))  # Ordena a fila com base no custo do caminho percorrido até o estado atual e na função heurística
        esatdo_atual, caminho = queue.popleft()  # Remove o estado com maior prioridade da fila

        if esatdo_atual.is_goal():  # Verifica se o estado atual é o estado objetivo
            return caminho, caminhos  # Retorna o caminho da solução e a lista de caminhos percorridos

        visitados.add(esatdo_atual)  # Adiciona o estado atual aos estados visitados
        sucessores = esatdo_atual.successors()  # Gera os estados sucessores do estado atual

        for sucessor, acao in sucessores:
            if sucessor not in visitados:  # Verifica se o sucessor já foi visitado
                queue.append((sucessor, caminho + [acao]))  # Adiciona o sucessor à fila com o caminho atualizado

        caminhos.append(caminho + [esatdo_atual])  # Adiciona o caminho percorrido até o estado atual à lista de caminhos

    return None, caminhos  # Retorna None para indicar que não foi encontrada uma solução e a lista de caminhos percorridos

print("Busca A*: ")
solucao_a_estrela, caminhos = busca_a_estrela()

if solucao_a_estrela:
    lado = False
    for i, acao in enumerate(solucao_a_estrela):
        lado = not lado
        print(f"Passo {i+1}: Leve {acao[0]} missionarios e {acao[1]} canibais para o lado {'direito' if lado else 'esquerdo'}.")
else:
    print("Não foi encontrada uma solução para o problema usando A* Search.")