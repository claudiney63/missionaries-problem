import time
import psutil


class Estado:
    def __init__(self, missionarios_esquerda, canibais_esquerda, missionarios_direita, canibais_direita, barco_na_esquerda, estado_pai=None):
        self.missionarios_esquerda = missionarios_esquerda
        self.canibais_esquerda = canibais_esquerda
        self.missionarios_direita = missionarios_direita
        self.canibais_direita = canibais_direita
        self.barco_na_esquerda = barco_na_esquerda
        self.estado_pai = estado_pai

    def e_valido(self):
        if (
            self.missionarios_esquerda < 0
            or self.canibais_esquerda < 0
            or self.missionarios_direita < 0
            or self.canibais_direita < 0
        ):
            return False
        if (
            self.missionarios_esquerda > 0
            and self.missionarios_esquerda < self.canibais_esquerda
            or self.missionarios_direita > 0
            and self.missionarios_direita < self.canibais_direita
        ):
            return False
        return True

    def e_estado_final(self):
        return (
            self.missionarios_esquerda == 0
            and self.canibais_esquerda == 0
            and self.missionarios_direita == self.canibais_direita
        )

    def __str__(self):
        return f"[{self.missionarios_esquerda}, {self.canibais_esquerda}, {self.missionarios_direita}, {self.canibais_direita}, {'Esquerda' if self.barco_na_esquerda else 'Direita'}]"


def resolver_bfs(num_missionarios, num_canibais):
    inicio = time.time()

    estado_inicial = Estado(num_missionarios, num_canibais, 0, 0, True)
    visitados = set()
    fila = [[estado_inicial]]
    nivel = 0
    nos_expandidos = 0
    nos_gerados = 0
    profundidade_maxima = 0
    uso_memoria_maximo = 0

    while fila:
        uso_memoria_maximo = max(uso_memoria_maximo, len(fila))
        caminho = fila.pop(0)
        print(f"Nível {nivel}:")
        nos_expandidos += 1

        estado_atual = caminho[-1]
        visitados.add(str(estado_atual))

        if estado_atual.e_estado_final():
            tempo_execucao = time.time() - inicio
            profundidade_solucao = len(caminho) - 1
            return caminho, nos_expandidos, nos_gerados, uso_memoria_maximo, nivel, profundidade_solucao, profundidade_maxima, tempo_execucao

        movimentos_possiveis = obter_movimentos_possiveis(estado_atual)
        for movimento in movimentos_possiveis:
            novo_estado = aplicar_movimento(estado_atual, movimento)
            indicador_valido = "Permitido" if novo_estado.e_valido() else ""
            print(f"{estado_atual} - {novo_estado} {indicador_valido} ")

            if str(novo_estado) not in visitados:
                nos_gerados += 1
                if novo_estado.e_valido():
                    fila.append(caminho + [novo_estado])
                    profundidade_maxima = max(profundidade_maxima, len(caminho))

        nivel += 1

    return None, nos_expandidos, nos_gerados, uso_memoria_maximo, nivel, 0, profundidade_maxima, tempo_execucao


def resolver_dfs(num_missionarios, num_canibais):
    inicio = time.time()

    estado_inicial = Estado(num_missionarios, num_canibais, 0, 0, True)
    visitados = set()
    pilha = [[estado_inicial]]
    nivel = 0
    nos_expandidos = 0
    nos_gerados = 0
    profundidade_maxima = 0
    uso_memoria_maximo = 0

    while pilha:
        uso_memoria_maximo = max(uso_memoria_maximo, len(pilha))
        caminho = pilha.pop()
        print(f"Nível {nivel}:")
        nos_expandidos += 1

        estado_atual = caminho[-1]
        visitados.add(str(estado_atual))

        if estado_atual.e_estado_final():
            tempo_execucao = time.time() - inicio
            profundidade_solucao = len(caminho) - 1
            return caminho, nos_expandidos, nos_gerados, uso_memoria_maximo, nivel, profundidade_solucao, profundidade_maxima, tempo_execucao

        movimentos_possiveis = obter_movimentos_possiveis(estado_atual)
        movimentos_possiveis.reverse()  
        for movimento in movimentos_possiveis:
            novo_estado = aplicar_movimento(estado_atual, movimento)
            indicador_valido = "Permitido" if novo_estado.e_valido() else ""
            print(f"{estado_atual} - {novo_estado} {indicador_valido}")

            if str(novo_estado) not in visitados:
                nos_gerados += 1
                if novo_estado.e_valido():
                    pilha.append(caminho + [novo_estado])
                    profundidade_maxima = max(profundidade_maxima, len(caminho))

        nivel += 1

    return None, nos_expandidos, nos_gerados, uso_memoria_maximo, nivel, 0, profundidade_maxima, tempo_execucao


def obter_movimentos_possiveis(estado):
    movimentos_possiveis = []
    if estado.barco_na_esquerda:
        for m in range(estado.missionarios_esquerda + 1):
            for c in range(estado.canibais_esquerda + 1):
                if m + c >= 1 and m + c <= 2:
                    movimentos_possiveis.append((m, c))
    else:
        for m in range(estado.missionarios_direita + 1):
            for c in range(estado.canibais_direita + 1):
                if m + c >= 1 and m + c <= 2:
                    movimentos_possiveis.append((m, c))
    return movimentos_possiveis


def aplicar_movimento(estado, movimento):
    if estado.barco_na_esquerda:
        novo_estado = Estado(
            estado.missionarios_esquerda - movimento[0],
            estado.canibais_esquerda - movimento[1],
            estado.missionarios_direita + movimento[0],
            estado.canibais_direita + movimento[1],
            not estado.barco_na_esquerda,
            estado
        )
    else:
        novo_estado = Estado(
            estado.missionarios_esquerda + movimento[0],
            estado.canibais_esquerda + movimento[1],
            estado.missionarios_direita - movimento[0],
            estado.canibais_direita - movimento[1],
            not estado.barco_na_esquerda,
            estado
        )
    return novo_estado


def exibir_caminho(caminho):
    print("Caminho da solução:")
    for i, estado in enumerate(caminho):
        print(f"{i}. {estado}")
    print(f"Total de passos: {len(caminho) - 1}")


def exibir_estatisticas(nos_expandidos, nos_gerados, uso_memoria_maximo, nivel, profundidade_solucao, profundidade_maxima, tempo_execucao):
    print(f"Nós expandidos: {nos_expandidos}")
    print(f"Nós gerados: {nos_gerados}")
    print(f"Nível da solução: {nivel}")
    print(f"Profundidade da solução: {profundidade_solucao}")
    print(f"Profundidade máxima: {profundidade_maxima}")
    print(f"Tempo de execução: {tempo_execucao:.6f} segundos")


def calcular_memoria_utilizada():
    process = psutil.Process()
    memoria_bytes = process.memory_info().rss
    memoria_mb = memoria_bytes / (1024 * 1024)
    return memoria_mb

def main():
    num_missionarios = 3
    num_canibais = 3

    print("Resolvendo com BFS:")
    resultado_bfs = resolver_bfs(num_missionarios, num_canibais)
    if resultado_bfs[0] is not None:
        caminho_bfs, nos_expandidos_bfs, nos_gerados_bfs, uso_memoria_maximo_bfs, nivel_bfs, profundidade_solucao_bfs, profundidade_maxima_bfs, tempo_execucao_bfs = resultado_bfs
        exibir_caminho(caminho_bfs)
        exibir_estatisticas(nos_expandidos_bfs, nos_gerados_bfs, uso_memoria_maximo_bfs, nivel_bfs, profundidade_solucao_bfs, profundidade_maxima_bfs, tempo_execucao_bfs)
        memoria_utilizada_bfs = calcular_memoria_utilizada()
        print(f"Memória utilizada (BFS): {memoria_utilizada_bfs:.2f} MB")
    else:
        print("Não foi encontrada uma solução com BFS.")

    print("\nResolvendo com DFS:")
    resultado_dfs = resolver_dfs(num_missionarios, num_canibais)
    if resultado_dfs[0] is not None:
        caminho_dfs, nos_expandidos_dfs, nos_gerados_dfs, uso_memoria_maximo_dfs, nivel_dfs, profundidade_solucao_dfs, profundidade_maxima_dfs, tempo_execucao_dfs = resultado_dfs
        exibir_caminho(caminho_dfs)
        exibir_estatisticas(nos_expandidos_dfs, nos_gerados_dfs, uso_memoria_maximo_dfs, nivel_dfs, profundidade_solucao_dfs, profundidade_maxima_dfs, tempo_execucao_dfs)
        memoria_utilizada_dfs = calcular_memoria_utilizada()
        print(f"Memória utilizada (DFS): {memoria_utilizada_dfs:.2f} MB")
    else:
        print("Não foi encontrada uma solução com DFS.")

if __name__ == "__main__":
    main()