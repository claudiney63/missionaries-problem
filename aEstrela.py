from collections import deque
import Estado
import psutil
import time

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
    nós_gerados = 0  # Variável para contar o número de nós gerados
    nós_expandidos = 0  # Variável para contar o número de nós expandidos
    nós_fronteira = 0  # Variável para contar o número de nós na fronteira

    while queue:
        queue = deque(sorted(queue, key=lambda x: len(x[1]) + heuristica(x[0])))  # Ordena a fila com base no custo do caminho percorrido até o estado atual e na função heurística
        estado_atual, caminho = queue.popleft()  # Remove o estado com maior prioridade da fila
        nós_fronteira -= 1  # Remove o nó atual da fronteira
        nós_expandidos += 1  # Incrementa o número de nós expandidos

        if estado_atual.is_goal():  # Verifica se o estado atual é o estado objetivo
            return caminho, caminhos, nós_gerados, nós_expandidos, nós_fronteira  # Retorna o caminho da solução, a lista de caminhos percorridos, o número de nós gerados, o número de nós expandidos e o número de nós na fronteira

        visitados.add(estado_atual)  # Adiciona o estado atual aos estados visitados
        sucessores = estado_atual.successors()  # Gera os estados sucessores do estado atual

        for sucessor, acao in sucessores:
            if sucessor not in visitados:  # Verifica se o sucessor já foi visitado
                queue.append((sucessor, caminho + [acao]))  # Adiciona o sucessor à fila com o caminho atualizado
                nós_fronteira += 1  # Incrementa o número de nós na fronteira
                nós_gerados += 1  # Incrementa a contagem de nós gerados

        caminhos.append(caminho + [estado_atual])  # Adiciona o caminho percorrido até o estado atual à lista de caminhos

    return None, caminhos, nós_gerados, nós_expandidos, nós_fronteira  # Retorna None para indicar que não foi encontrada uma solução, a lista de caminhos percorridos, o número de nós gerados, o número de nós expandidos e o número de nós na fronteira

print("Busca A*: ")
inicio = time.time()
memoria_inicial = calcular_memoria_utilizada()
print(f"Utilização de memória antes: {memoria_inicial} MB")

solucao_a_estrela, caminhos, nos_gerados, nos_expandidos, nos_fronteira = busca_a_estrela()

fim = time.time()
tempo_execucao = fim - inicio

memoria_final = calcular_memoria_utilizada()
print(f"Utilização de memória depois: {memoria_final} MB")

diferenca_memoria = memoria_final - memoria_inicial
print(f"Diferença de memória: {diferenca_memoria} MB")
print(f"Tempo de execução: {tempo_execucao} segundos")

if solucao_a_estrela:
    lado = False
    for i, acao in enumerate(solucao_a_estrela):
        lado = not lado
        print(f"Passo {i+1}: Leve {acao[0]} missionários e {acao[1]} canibais para o lado {'direito' if lado else 'esquerdo'}.")
else:
    print("Não foi encontrada uma solução para o problema usando A* Search.")

print("Número de nós gerados:", nos_gerados)
print("Número de nós expandidos:", nos_expandidos)
print("Número de nós na fronteira:", nos_fronteira)
