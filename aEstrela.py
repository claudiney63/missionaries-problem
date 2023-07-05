import heapq
import psutil
import time


class Estado:
    def __init__(self, missionarios_esquerda, canibais_esquerda, missionarios_direita, canibais_direita, barco_na_esquerda):
        self.missionarios_esquerda = missionarios_esquerda
        self.canibais_esquerda = canibais_esquerda
        self.missionarios_direita = missionarios_direita
        self.canibais_direita = canibais_direita
        self.barco_na_esquerda = barco_na_esquerda

    def eh_valido(self):
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

    def eh_objetivo(self):
        return (
            self.missionarios_esquerda == 0
            and self.canibais_esquerda == 0
            and self.missionarios_direita == self.canibais_direita
        )

    def __str__(self):
        return f"[{self.missionarios_esquerda}, {self.canibais_esquerda}, {self.missionarios_direita}, {self.canibais_direita}, {'Esquerda' if self.barco_na_esquerda else 'Direita'}]"


class No:
    def __init__(self, estado, pai=None, acao=None, g=0, h=0):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.g = g
        self.h = h

    def __lt__(self, outro):
        return self.g + self.h < outro.g + outro.h


def resolver(num_missionarios, num_canibais):
    estado_inicial = Estado(num_missionarios, num_canibais, 0, 0, True)
    no_inicial = No(estado_inicial)
    visitados = set()
    fila = []
    heapq.heappush(fila, no_inicial)

    # Estatísticas
    nos_expandidos = 0
    nos_gerados = 0
    uso_maximo_memoria = 0
    profundidade_maxima = 0
    profundidade_solucao = 0

    while fila:
        no_atual = heapq.heappop(fila)
        estado_atual = no_atual.estado
        nos_expandidos += 1
        uso_maximo_memoria = max(uso_maximo_memoria, len(fila))
        profundidade_maxima = max(profundidade_maxima, no_atual.g)

        if estado_atual.eh_objetivo():
            caminho = []
            while no_atual:
                caminho.append(no_atual.estado)
                no_atual = no_atual.pai
            caminho.reverse()
            profundidade_solucao = len(caminho) - 1
            return caminho, nos_expandidos, nos_gerados, uso_maximo_memoria, profundidade_maxima, profundidade_solucao

        visitados.add(str(estado_atual))

        movimentos_possiveis = obter_movimentos_possiveis(estado_atual)
        for movimento in movimentos_possiveis:
            novo_estado = aplicar_movimento(estado_atual, movimento)
            indicador_valido = "Permitido" if novo_estado.eh_valido() else ""
            print(f'{estado_atual} - {novo_estado} {indicador_valido} ')

            if str(novo_estado) not in visitados:
                nos_gerados += 1
                if novo_estado.eh_valido():
                    novo_no = No(
                        novo_estado,
                        pai=no_atual,
                        acao=movimento,
                        g=no_atual.g + 1,
                        h=calcular_heuristica(novo_estado),
                    )
                    visitados.add(str(novo_estado))
                    heapq.heappush(fila, novo_no)

    return None, nos_expandidos, nos_gerados, uso_maximo_memoria, profundidade_maxima, profundidade_solucao


def obter_movimentos_possiveis(estado):
    movimentos_possiveis = []
    if estado.barco_na_esquerda:
        for m in range(estado.missionarios_esquerda + 1):
            for c in range(estado.canibais_esquerda + 1):
                if 1 <= m + c <= 2:
                    movimentos_possiveis.append((m, c))
    else:
        for m in range(estado.missionarios_direita + 1):
            for c in range(estado.canibais_direita + 1):
                if 1 <= m + c <= 2:
                    movimentos_possiveis.append((m, c))
    return movimentos_possiveis


def aplicar_movimento(estado, movimento):
    missionarios, canibais = movimento
    if estado.barco_na_esquerda:
        novo_missionarios_esquerda = estado.missionarios_esquerda - missionarios
        novo_canibais_esquerda = estado.canibais_esquerda - canibais
        novo_missionarios_direita = estado.missionarios_direita + missionarios
        novo_canibais_direita = estado.canibais_direita + canibais
        novo_barco_na_esquerda = False
    else:
        novo_missionarios_esquerda = estado.missionarios_esquerda + missionarios
        novo_canibais_esquerda = estado.canibais_esquerda + canibais
        novo_missionarios_direita = estado.missionarios_direita - missionarios
        novo_canibais_direita = estado.canibais_direita - canibais
        novo_barco_na_esquerda = True
    return Estado(novo_missionarios_esquerda, novo_canibais_esquerda, novo_missionarios_direita, novo_canibais_direita, novo_barco_na_esquerda)


def calcular_heuristica(estado):
    return estado.missionarios_esquerda + estado.canibais_esquerda

if __name__ == "__main__":
    num_missionarios = 3
    num_canibais = 3

    # Obter o uso de memória antes da execução
    process = psutil.Process()
    initial_memory_usage = process.memory_info().rss

    start_time = time.time()

    solucao, nos_expandidos, nos_gerados, uso_maximo_memoria, profundidade_maxima, profundidade_solucao = resolver(
        num_missionarios, num_canibais
    )

    end_time = time.time()

    # Obter o uso de memória após a execução
    final_memory_usage = process.memory_info().rss

    # Calcular o uso de memória durante a execução em megabytes
    memory_usage = (final_memory_usage - initial_memory_usage) / 1024 / 1024

    # Calcular o tempo de execução em segundos
    execution_time = end_time - start_time

    if solucao:
        print("Caminho:")
        for estado in solucao:
            print(estado)
    else:
        print("Nenhuma solução encontrada.")

    print("Nós expandidos:", nos_expandidos)
    print("Nós gerados:", nos_gerados)
    print("Uso de memória:", memory_usage, "MB")
    print("Profundidade máxima:", profundidade_maxima)
    print("Profundidade da solução:", profundidade_solucao)
    print("Tempo de execução:", execution_time, "segundos")
