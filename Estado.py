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