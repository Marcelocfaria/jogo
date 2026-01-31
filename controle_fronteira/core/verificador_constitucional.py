# core/verificador_constitucional.py
from core.enums import Nacionalidade, TipoCargo, StatusPolitico, TipoCrime

class Verificador:
    @staticmethod
    def validar(personagem):
        # --- 1. REGRA: DIREITOS POLÍTICOS ---
        if personagem.status_politico == StatusPolitico.SUSPENSO:
            return False, "Direitos políticos suspensos!"
        
        # --- 2. REGRA: BRASILEIROS NATOS (Art. 12, §3º) ---
        cargos_so_natos = [
            TipoCargo.PRESIDENTE,
            TipoCargo.PRESIDENTE_CAMARA_DEPUTADOS,
            TipoCargo.PRESIDENTE_SENADO,
            TipoCargo.MINISTRO_STF,
            TipoCargo.CARREIRA_DIPLOMATICA,
            TipoCargo.OFICIAL_FORCAS_ARMADAS,
            TipoCargo.MINISTRO_DEFESA
        ]
        if personagem.cargo_pretendido in cargos_so_natos and personagem.nacionalidade != Nacionalidade.NATO:
            return False, "Este cargo é exclusivo para Brasileiros Natos!"
        
        # --- 3. REGRA: IDADE MÍNIMA (Art. 14, §3º, VI) ---
        cargo = personagem.cargo_pretendido
        idade = personagem.idade
        
        # 35 anos - Presidente e Senador
        if cargo in [TipoCargo.PRESIDENTE, TipoCargo.SENADOR]:
            if idade < 35: 
                return False, "Idade mínima de 35 anos!"
        
        # 30 anos - Governador
        elif cargo == TipoCargo.GOVERNADOR:
            if idade < 30: 
                return False, "Idade mínima de 30 anos!"
        
        # 21 anos - Deputado Federal, Deputado Estadual e Prefeito
        elif cargo in [TipoCargo.PREFEITO, TipoCargo.DEPUTADO_FEDERAL, TipoCargo.DEPUTADO_ESTADUAL]:
            if idade < 21: 
                return False, "Idade mínima de 21 anos!"
        
        # 18 anos - Vereador
        elif cargo == TipoCargo.VEREADOR:
            if idade < 18: 
                return False, "Idade mínima de 18 anos!"
        
        # --- 4. REGRA ESPECÍFICA: Ministro STF (Art. 101, CF/88) ---
        # Idade mínima de 35 anos e máxima de 65 anos
        if cargo == TipoCargo.MINISTRO_STF:
            if idade < 35:
                return False, "Ministro do STF: idade mínima de 35 anos!"
            if idade > 65:
                return False, "Ministro do STF: idade máxima de 65 anos!"
        
        # --- 5. REGRA: Presidente da Câmara e do Senado ---
        # Devem ser Deputados ou Senadores respectivamente (logo, já têm idade mínima atendida)
        # Mas vamos validar explicitamente
        if cargo == TipoCargo.PRESIDENTE_CAMARA_DEPUTADOS:
            if idade < 21:  # Mesma idade mínima de Deputado Federal
                return False, "Presidente da Câmara: idade mínima de 21 anos!"
        
        if cargo == TipoCargo.PRESIDENTE_SENADO:
            if idade < 35:  # Mesma idade mínima de Senador
                return False, "Presidente do Senado: idade mínima de 35 anos!"
        
        # --- 6. REGRA ESPECÍFICA: Cargos não eleitorais ---
        # Carreira Diplomática, Oficial das Forças Armadas, Ministro da Defesa, Comum
        # Têm requisitos próprios, mas mantendo idade mínima de 18 anos
        if cargo in [TipoCargo.CARREIRA_DIPLOMATICA, TipoCargo.OFICIAL_FORCAS_ARMADAS, 
                     TipoCargo.MINISTRO_DEFESA, TipoCargo.COMUM]:
            if idade < 18: 
                return False, "Cidadão deve ser maior de idade!"
        
        # --- 7. REGRA: EXTRADIÇÃO ---
        if personagem.crime == TipoCrime.POLITICO:
            return False, "Vedada extradição por crime político!"
        
        return True, "Ficha em conformidade constitucional."