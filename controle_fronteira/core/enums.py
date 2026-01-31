# core/enums.py
from enum import Enum

class Nacionalidade(Enum):
    NATO = "Nato"
    NATURALIZADO = "Naturalizado"
    ESTRANGEIRO = "Estrangeiro"

class TipoCargo(Enum):
    VEREADOR = "Vereador"
    PREFEITO = "Prefeito"
    GOVERNADOR = "Governador"
    DEPUTADO_FEDERAL = "Deputado Federal"
    DEPUTADO_ESTADUAL = "Deputado Estadual"
    SENADOR = "Senador"
    PRESIDENTE = "Presidente"
    MINISTRO_STF = "Ministro do STF"       # Privado de Nato
    CARREIRA_DIPLOMATICA = "Diplomata"     # Privado de Nato
    COMUM = "Analista Administrativo"      # Qualquer um
    OFICIAL_FORCAS_ARMADAS = "Oficial das Forças Armadas"
    MINISTRO_DEFESA = "Ministro da Defesa"
    PRESIDENTE_SENADO = "Presidente do Senado"
    PRESIDENTE_CAMARA_DEPUTADOS = "Presidente da Camara dos Deputados"
class StatusPolitico(Enum):
    REGULAR = "Regular"
    SUSPENSO = "Suspenso"

class TipoCrime(Enum):
    NENHUM = "Nenhum"
    COMUM = "Crime Comum (Roubo)"
    POLITICO = "Crime Político / Opinião"