from collections import deque

class Estado:
    def __init__(self, missionarios, canibais, barco_esquerda):
        self.missionarios = missionarios
        self.canibais = canibais
        self.barco_esquerda = barco_esquerda

    def is_valid(self):
        """
            O método is_valid() verifica se o estado é válido (ou seja, se não há mais canibais do que missionários em qualquer margem)
        """
        if self.missionarios < 0 or self.canibais < 0 or self.missionarios > 3 or self.canibais > 3:
            return False
        if self.missionarios > 0 and self.missionarios < self.canibais:
            return False
        if self.missionarios < 3 and (3 - self.missionarios) < (3 - self.canibais):
            return False
        return True

    def is_goal(self):
        """
        Método is_goal() verifica se é o estado objetivo (todos os missionários e canibais estão na margem oposta). 
        """
        return self.missionarios == 0 and self.canibais == 0 and not self.barco_esquerda

    def successors(self):
        """
        O método successors() gera todos os possíveis estados sucessores a partir do estado atual.
        """
        successors = []
        if self.barco_esquerda:
            for m in range(3):
                for c in range(3):
                    if 1 <= m + c <= 2:
                        new_state = Estado(self.missionarios - m, self.canibais - c, not self.barco_esquerda)
                        if new_state.is_valid():
                            successors.append((new_state, (m, c)))
        else:
            for m in range(3):
                for c in range(3):
                    if 1 <= m + c <= 2:
                        new_state = Estado(self.missionarios + m, self.canibais + c, not self.barco_esquerda)
                        if new_state.is_valid():
                            successors.append((new_state, (m, c)))
        return successors

def encontrar_solucao():
    """
    A função encontrar_solucao() utiliza a busca em largura (BFS) para explorar todos os estados possíveis 
    até encontrar uma solução. Ela mantém uma fila de estados a serem explorados e uma lista de estados visitados 
    para evitar ciclos. A função retorna uma lista de ações que levam à solução, indicando quantos missionários e 
    canibais devem ser levados de uma margem para a outra em cada passo.
    """
    initial_state = Estado(3, 3, True)
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

solucao = encontrar_solucao()
if solucao:
    for i, acao in enumerate(solucao):
        print(f"Passo {i+1}: Leve {acao[0]} missionarios e {acao[1]} canibais para o outro lado.")
else:
    print("Não foi encontrada uma solução para o problema.")
