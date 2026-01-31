# core/gerador_casos.py
import random
from core.personagem import Personagem
from core.enums import Nacionalidade, TipoCargo, StatusPolitico, TipoCrime

class GeradorCasos:
    def __init__(self):
        self.nomes = ["Ana", "Carlos", "Beatriz", "João", "Helena", "Marcos"]
        self.sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Pereira"]

    def gerar_caso(self):
        nome_completo = f"{random.choice(self.nomes)} {random.choice(self.sobrenomes)}"
        idade = random.randint(16, 50)
        nacionalidade = random.choice(list(Nacionalidade))
        cargo = random.choice(list(TipoCargo))
        status = random.choice([StatusPolitico.REGULAR, StatusPolitico.REGULAR, StatusPolitico.SUSPENSO])
        crime_aleatorio = random.choice(list(TipoCrime))


        return Personagem(nome_completo, idade, nacionalidade, cargo, status, crime_aleatorio)