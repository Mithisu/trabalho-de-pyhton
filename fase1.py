import pygame
import sys
import random
from jogador import criar_jogador, mover_jogador, checar_interacoes
from fase2 import fase2  # Importa a próxima fase
from pause_menu import pause_menu  # Importa a tela de pause

# Funções para gerar diferentes tipos de equações matemáticas
def gerar_equacao_soma():
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    pergunta = f"{num1} + {num2}"
    resposta = num1 + num2
    return {"pergunta": pergunta, "resposta": resposta}

def gerar_equacao_subtracao():
    num1 = random.randint(1, 20)
    num2 = random.randint(1, num1)  # Garante que o resultado não seja negativo
    pergunta = f"{num1} - {num2}"
    resposta = num1 - num2
    return {"pergunta": pergunta, "resposta": resposta}

def gerar_equacao_multiplicacao():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    pergunta = f"{num1} * {num2}"
    resposta = num1 * num2
    return {"pergunta": pergunta, "resposta": resposta}

def gerar_equacao_divisao():
    num2 = random.randint(1, 10)
    resposta = random.randint(1, 10)
    num1 = resposta * num2  # Garante que a divisão seja exata
    pergunta = f"{num1} / {num2}"
    return {"pergunta": pergunta, "resposta": resposta}

# Gera uma alternativa errada (diferente da resposta correta)
def gerar_alternativa_errada(valor_correto, minimo=0, maximo=100):
    while True:
        valor_errado = random.randint(minimo, maximo)
        if valor_errado != valor_correto:
            return valor_errado

# Função principal da fase 1
def fase1():
    pygame.init()
    tela = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Missão: Código Secreto - Fase 1")

    # Tenta carregar fonte personalizada, senão usa padrão
    try:
        pixel_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 32)
    except:
        pixel_font = pygame.font.SysFont("Courier", 32)

    WORLD_WIDTH = 2560
    WORLD_HEIGHT = 1440

    # Cria jogador
    player, player_speed = criar_jogador(WORLD_WIDTH, WORLD_HEIGHT)
    jogador_carregando = None  # Guarda item carregado (resposta)

    # Gera as equações da fase
    equacoes = [
        gerar_equacao_soma(),
        gerar_equacao_subtracao(),
        gerar_equacao_multiplicacao(),
        gerar_equacao_divisao(),
    ]

    # Define posição de cada equação no mapa
    for eq in equacoes:
        eq["rect"] = pygame.Rect(random.randint(100, WORLD_WIDTH - 100),
                                 random.randint(100, WORLD_HEIGHT - 100), 160, 60)
        eq["resolvida"] = False

    respostas = []

    # Cria duas alternativas (uma correta e uma errada) para cada equação
    for eq in equacoes:
        respostas.append({
            "valor": eq["resposta"],
            "rect": pygame.Rect(random.randint(100, WORLD_WIDTH - 100),
                                random.randint(100, WORLD_HEIGHT - 100), 50, 50)
        })
        valor_errado = gerar_alternativa_errada(eq["resposta"], minimo=0, maximo=100)
        respostas.append({
            "valor": valor_errado,
            "rect": pygame.Rect(random.randint(100, WORLD_WIDTH - 100),
                                random.randint(100, WORLD_HEIGHT - 100), 50, 50)
        })

    porta = pygame.Rect(2400, 1200, 100, 100)  # Porta de saída da fase
    porta_ativa = False  # Só aparece quando todas as equações forem resolvidas

    pontos = 0
    clock = pygame.time.Clock()
    running = True

    # Loop principal do jogo
    while running:
        tela.fill((30, 30, 30))  # Cor de fundo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Pausar o jogo
                fase_atual = 1
                acao_pause = pause_menu(tela, pixel_font, fase_atual)
                if acao_pause == "menu":
                    return "menu"

        # Atualiza movimento e interações
        keys = pygame.key.get_pressed()
        player = mover_jogador(player, player_speed, keys, WORLD_WIDTH, WORLD_HEIGHT)
        coletar, dropar = checar_interacoes(keys)

        # Câmera: calcula o deslocamento da tela com base no jogador
        offset_x = player.x - 1280 // 2 + player.width // 2
        offset_y = player.y - 720 // 2 + player.height // 2

        # Pegando resposta
        if jogador_carregando is None:
            for resposta in respostas:
                if player.colliderect(resposta["rect"]) and coletar:
                    jogador_carregando = resposta
                    respostas.remove(resposta)
                    break

        # Soltando resposta
        if jogador_carregando and dropar:
            jogador_carregando["rect"].x = player.x + player.width // 2 - jogador_carregando["rect"].width // 2
            jogador_carregando["rect"].y = player.y + player.height // 2 - jogador_carregando["rect"].height // 2
            respostas.append(jogador_carregando)
            jogador_carregando = None

        # Tentativa de entrega de resposta
        if jogador_carregando:
            for eq in equacoes:
                if player.colliderect(eq["rect"]) and not eq["resolvida"]:
                    if jogador_carregando["valor"] == eq["resposta"]:
                        pontos += 1
                        eq["resolvida"] = True
                        jogador_carregando = None
                    else:
                        jogador_carregando = None
                    break

        # Desenha equações
        for eq in equacoes:
            cor = (0, 255, 0) if eq["resolvida"] else (255, 100, 100)
            rect = eq["rect"].copy()
            rect.x -= offset_x
            rect.y -= offset_y
            pygame.draw.rect(tela, cor, rect)
            texto = pixel_font.render(eq["pergunta"], True, (0, 0, 0))
            tela.blit(texto, (rect.x + 10, rect.y + 15))

        # Desenha respostas
        for resposta in respostas:
            rect = resposta["rect"].copy()
            rect.x -= offset_x
            rect.y -= offset_y
            pygame.draw.rect(tela, (255, 255, 0), rect)
            texto = pixel_font.render(str(resposta["valor"]), True, (0, 0, 0))
            tela.blit(texto, (rect.x + 5, rect.y + 5))

        # Desenha jogador fixo no centro da tela
        player_rect_tela = pygame.Rect(1280 // 2 - player.width // 2,
                                       720 // 2 - player.height // 2, player.width, player.height)
        pygame.draw.rect(tela, (0, 200, 255), player_rect_tela)

        # Exibe valor carregado
        if jogador_carregando:
            texto_item = pixel_font.render(f"Carregando: {jogador_carregando['valor']}", True, (255, 255, 255))
            tela.blit(texto_item, (20, 660))

        # Ativa a porta quando todas forem resolvidas
        if pontos == len(equacoes):
            porta_ativa = True

        # Desenha a porta (se ativa)
        if porta_ativa:
            porta_rect_tela = porta.copy()
            porta_rect_tela.x -= offset_x
            porta_rect_tela.y -= offset_y
            pygame.draw.rect(tela, (0, 0, 255), porta_rect_tela)
            texto_porta = pixel_font.render("Ir para próxima fase", True, (0, 0, 0))
            tela.blit(texto_porta, (porta_rect_tela.x + 10, porta_rect_tela.y + 35))

        # Verifica se jogador entrou na porta para ir pra fase 2
        if porta_ativa and player.colliderect(porta):
            retorno = fase2()
            if retorno == "menu":
                return "menu"

        # Exibe pontuação
        texto_pontos = pixel_font.render(f"Pontos: {pontos}", True, (255, 255, 255))
        tela.blit(texto_pontos, (1080, 20))

        # Atualiza tela
        pygame.display.flip()
        clock.tick(60)
