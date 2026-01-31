# main.py
import pygame
import sys
from settings import *
from core.personagem import Personagem
from core.enums import Nacionalidade, TipoCargo
from core.verificador_constitucional import Verificador
from core.gerador_casos import GeradorCasos
from core.enums import StatusPolitico


def main():
    # Inicializa o Pygame
    pygame.init()
    
    # Inicializa o mixer de áudio
    pygame.mixer.init()
    # som_carimbo = pygame.mixer.Sound("assets/carimbo.wav") # Descomente quando tiver o arquivo

    # Cria a janela
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    try:
        img_mesa = pygame.image.load("assets/mesa.png").convert_alpha()
        img_mesa = pygame.transform.scale(img_mesa, (SCREEN_WIDTH, 400))
    except:
        # Caso a imagem não exista, ele cria um retângulo marrom para o jogo não travar
        img_mesa = pygame.Surface((SCREEN_WIDTH, 400))
        img_mesa.fill((139, 69, 19))
    pygame.display.set_caption("CONSTITUIÇÃO: CONTROLE DE FRONTEIRA")
    
    
    clock = pygame.time.Clock()
    running = True

    gerador = GeradorCasos()
    caso_atual = gerador.gerar_caso()
    fonte = pygame.font.SysFont("Arial", 24)

    # No main.py, antes do loop:
    btn_aprovar = pygame.Rect(900, 500, 150, 60) # x, y, largura, altura
    btn_negar = pygame.Rect(900, 600, 150, 60)

    cor_btn_aprovar = (46, 139, 87) # Verde
    cor_btn_negar = (178, 34, 34)   # Vermelho

# 2. Variáveis de Estado (Dinheiro, Tempo, Erros)
    saldo = 100
    erros_cometidos = 0
    tempo_restante = 60  # Segundos de jogo
    timer_evento = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_evento, 1000) # Dispara a cada 1000ms (1 segundo)
    game_over = False
    motivo_demissao = ""

    # LOOP PRINCIPAL DO JOGO
    while running:
        # --- 1. CHECAGEM DE ESTADO (Onde entra a parte nova) ---
        if not game_over:
            if saldo < 0:
                game_over = True
                motivo_demissao = "DÉFICIT NO ORÇAMENTO PÚBLICO"
            elif erros_cometidos >= 5:
                game_over = True
                motivo_demissao = "DESCUMPRIMENTO CONSTITUCIONAL REITERADO"

        # 1. Captura de Eventos (Teclado, Mouse, Fechar Janela)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    # Reseta todas as variáveis para o estado inicial
                    saldo = 100
                    erros_cometidos = 0
                    tempo_restante = 60
                    game_over = False
                    caso_atual = gerador.gerar_caso()

            if event.type == timer_evento and not game_over:
                tempo_restante -= 1
                if tempo_restante <= 0:
                    # Se o tempo acabar, checamos se o jogador atingiu uma meta
                    if saldo < 150: # Exemplo: meta de 150 reais
                        game_over = True
                        motivo_demissao = "BAIXA PRODUTIVIDADE NO EXPEDIENTE"
                    else:
                        # Se passou da meta, ganhamos mais tempo (próximo dia)
                        tempo_restante = 60
                        saldo += 50 # Bônus de fim de dia
            if event.type == pygame.QUIT:
                running = False
            
            # Processa cliques apenas se não estiver em game_over
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos 
                
                # --- BOTÃO APROVAR ---
                if btn_aprovar.collidepoint(mouse_pos):
                    correto, motivo = Verificador.validar(caso_atual)
                    if correto: # Acertou
                        saldo += 10
                        # Balanceamento aqui: o tempo sobe, mas trava em 60s
                        tempo_restante = min(tempo_restante + 5, 60)
                        print(f"✅ BOA! {motivo}")
                    else: # Errou
                        saldo -= 15
                        erros_cometidos += 1
                        print(f"❌ ERROU! {motivo}")
                    caso_atual = gerador.gerar_caso()

                # --- BOTÃO NEGAR ---
                elif btn_negar.collidepoint(mouse_pos):
                    correto, motivo = Verificador.validar(caso_atual)
                    if not correto: # Acertou
                        saldo += 10
                        # Balanceamento aqui também
                        tempo_restante = min(tempo_restante + 5, 60)
                        print(f"✅ BOA! {motivo}")
                    else: # Errou
                        saldo -= 15
                        erros_cometidos += 1
                        print(f"❌ ERROU! {motivo}")
                    caso_atual = gerador.gerar_caso()
        
        # 2. Atualização da Lógica (pode adicionar lógica adicional aqui)

        # --- 3. DESENHO (A ordem importa!) ---
        if not game_over:
            # 1º: Limpa a tela com a cor de fundo
            screen.fill(COLOR_BG) 
            
            # 2º: Desenha a mesa (o retângulo marrom)
            

            # 3º: Desenha os Textos do Cidadão (sobre a mesa)
            surface_nome = fonte.render(f"NOME: {caso_atual.nome}", True, (255, 255, 255))
            surface_cargo = fonte.render(f"CARGO: {caso_atual.cargo_pretendido.value}", True, (255, 255, 255))
            surface_nac = fonte.render(f"NACIONALIDADE: {caso_atual.nacionalidade.value}", True, (255, 255, 255))
            surface_politico = fonte.render(f"SITUAÇÃO POLÍTICA: {caso_atual.status_politico.value}", True, (255, 255, 255))
            surface_crime = fonte.render(f"FICHA CRIMINAL: {caso_atual.crime.value}", True, (255, 255, 255))         
            surface_idade = fonte.render(f"IDADE: {caso_atual.idade} ANOS", True, (255, 255, 255))

            screen.blit(img_mesa, (0, 50))
            screen.blit(surface_nome, (50, 480))
            screen.blit(surface_idade, (50, 520))  # 40px de distância
            screen.blit(surface_cargo, (50, 560))
            screen.blit(surface_nac, (50, 600))
            screen.blit(surface_politico, (50, 640))
            screen.blit(surface_crime, (50, 680))
            
            # 4º: DESENHA OS BOTÕES
            pygame.draw.rect(screen, cor_btn_aprovar, btn_aprovar)
            pygame.draw.rect(screen, cor_btn_negar, btn_negar)

            # Desenha o texto dentro do botão APROVAR
            txt_aprovar = fonte.render("APROVAR", True, (255, 255, 255))
            screen.blit(txt_aprovar, (btn_aprovar.x + 20, btn_aprovar.y + 15))

            # Desenha o texto dentro do botão NEGAR
            txt_negar = fonte.render("NEGAR", True, (255, 255, 255))
            screen.blit(txt_negar, (btn_negar.x + 35, btn_negar.y + 15))

            # Painel de Status (HUD)
            surface_saldo = fonte.render(f"SALDO: R$ {saldo}", True, (255, 215, 0))
            surface_erros = fonte.render(f"ERROS: {erros_cometidos}", True, (255, 50, 50))
            
            screen.blit(surface_saldo, (50, 20))
            screen.blit(surface_erros, (300, 20))

            # Desenha o cronômetro
            cor_relogio = (255, 255, 255)
            if tempo_restante < 10: cor_relogio = (255, 0, 0) # Fica vermelho no final
            
            surface_tempo = fonte.render(f"TEMPO: {tempo_restante}s", True, cor_relogio)
            screen.blit(surface_tempo, (1100, 20)) # No canto superior direito
        else:
            # TELA DE GAME OVER
            screen.fill((20, 20, 20))
            txt_fim = fonte.render("VOCÊ FOI EXONERADO!", True, (255, 0, 0))
            txt_motivo = fonte.render(motivo_demissao, True, (200, 200, 200))
            txt_recomecar = fonte.render("Pressione R para recomeçar", True, (255, 255, 255))
            
            screen.blit(txt_fim, (SCREEN_WIDTH//2 - 150, 200))
            screen.blit(txt_motivo, (SCREEN_WIDTH//2 - 200, 300))
            screen.blit(txt_recomecar, (SCREEN_WIDTH//2 - 150, 450))

        clock.tick(FPS) # Garante que o jogo rode suave a 60 frames por segundo
        # Atualiza o monitor (Deve ser a última linha DENTRO do loop while)
        pygame.display.flip()

    # FORA DO LOOP - Código de encerramento
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()