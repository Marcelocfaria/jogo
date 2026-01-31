# core/personagem.py
from core.enums import Nacionalidade

class Personagem:
    def __init__(self, nome, idade, nacionalidade, cargo_pretendido, status_politico, crime):
        self.nome = nome
        self.idade = idade
        self.nacionalidade = nacionalidade
        self.cargo_pretendido = cargo_pretendido
        self.status_politico = status_politico 
        self.crime = crime 

    def __str__(self):
        return f"{self.nome} | {self.idade} anos | {self.nacionalidade.value} | Almeja: {self.cargo_pretendido.value}"