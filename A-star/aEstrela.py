import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import Estado
import psutil
import sys

def calcular_memoria_utilizada():
    processo = psutil.Process()
    memoria = processo.memory_info().rss
    return memoria / (1024 * 1024)  # Converter para megabytes

def heuristica(estado):
    # Função heurística: número de missionários e canibais ainda na margem esquerda
    return estado.missionarios + estado.canibais

def busca_a_estrela():
    estado_inicial = Estado.Estado(3, 3, True)  # Cria um estado inicial com 3 missionários e 3 canibais na margem esquerda
    visitados = set()  # Conjunto para armazenar os estados visitados
    queue = deque([(estado_inicial, [])])  # Fila para armazenar os estados a serem explorados, com o estado inicial e um caminho vazio
    caminhos = []  # Lista para armazenar os caminhos percorridos em cada iteração
    nos_gerados = 0  # Variável para contar o número de nós gerados

    while queue:
        queue = deque(sorted(queue, key=lambda x: len(x[1]) + heuristica(x[0])))  # Ordena a fila com base no custo do caminho percorrido até o estado atual e na função heurística
        estado_atual, caminho = queue.popleft()  # Remove o estado com maior prioridade da fila

        if estado_atual.is_goal():  # Verifica se o estado atual é o estado objetivo
            return caminho, caminhos, nos_gerados  # Retorna o caminho da solução, a lista de caminhos percorridos e o número de nós gerados

        visitados.add(estado_atual)  # Adiciona o estado atual aos estados visitados
        sucessores = estado_atual.successors()  # Gera os estados sucessores do estado atual

        for sucessor, acao in sucessores:
            if sucessor not in visitados:  # Verifica se o sucessor já foi visitado
                queue.append((sucessor, caminho + [acao]))  # Adiciona o sucessor à fila com o caminho atualizado
                nos_gerados += 1  # Incrementa a contagem de nós gerados

        caminhos.append(caminho + [estado_atual])  # Adiciona o caminho percorrido até o estado atual à lista de caminhos

    return None, caminhos, nos_gerados  # Retorna None para indicar que não foi encontrada uma solução, a lista de caminhos percorridos e o número de nós gerados

# def plotar_caminhos(caminhos):
#     G = nx.DiGraph()

#     for caminho in caminhos:
#         for i in range(len(caminho)):
#             estado = caminho[i]
#             G.add_node(estado)

#             if i > 0:
#                 estado_anterior = caminho[i-1]
#                 G.add_edge(estado_anterior, estado)

#     pos = nx.spring_layout(G)

#     plt.figure(figsize=(10, 6))
#     nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
#     nx.draw_networkx_edges(G, pos, edge_color='gray')
#     nx.draw_networkx_labels(G, pos, font_size=10)

#     plt.axis('off')
#     plt.show()

print("Busca A*: ")
memoria_inicial = calcular_memoria_utilizada()
print(f"Utilizacao de memoria antes: {memoria_inicial} MB")

solucao_a_estrela, caminhos, nos_gerados = busca_a_estrela()

memoria_final = calcular_memoria_utilizada()
print(f"Utilizacao de memoria depois: {memoria_final} MB")

diferenca_memoria = memoria_final - memoria_inicial
print(f"Diferenca de memoria: {diferenca_memoria} MB")

if solucao_a_estrela:
    lado = False
    for i, acao in enumerate(solucao_a_estrela):
        lado = not lado
        print(f"Passo {i+1}: Leve {acao[0]} missionarios e {acao[1]} canibais para o lado {'direito' if lado else 'esquerdo'}.")
else:
    print("Não foi encontrada uma solução para o problema usando A* Search.")

print("Numero de nos gerados:", nos_gerados)

# # Plotar os caminhos
# plotar_caminhos(caminhos)