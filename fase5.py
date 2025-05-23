import pygame
import sys
import random
import math
from jogador import criar_jogador, mover_jogador, checar_interacoes
from pause_menu import pause_menu  # Importa a função do menu de pausa
from fim_de_jogo import tela_final  # Importa a tela final

# Função para gerar uma equação de 2º grau com soluções inteiras
def gerar_equacao_2_grau():
    while True:
        a = random.randint(1, 3)  # Coeficiente a
        b = random.randint(-10, 10)  # Coeficiente b
        c = random.randint(-10, 10)  # Coeficiente c
        delta = b**2 - 4 * a * c  # Calcula o discriminante da equação
        if delta >= 0:  # Verifica se o delta é positivo (equação tem raízes reais)
            x1 = (-b + math.sqrt(delta)) / (2 * a)  # Primeira solução
            x2 = (-b - math.sqrt(delta)) / (2 * a)  # Segunda solução
            # Verifica se ambas as soluções são inteiras
            if x1.is_integer() and x2.is_integer():
                pergunta = f"{a}x² + {b}x + {c} = 0"  # Forma da equação
                return {
                    "pergunta": pergunta,
                    "respostas": [int(x1), int(x2)],  # Respostas corretas
                    "resolvida": False,  # A equação ainda não foi resolvida
                    "rect": None  # A área onde a equação será mostrada
                }

# Função para a fase 5 do jogo
def fase5():
    pygame.init()  # Inicializa o Pygame
    tela = pygame.display.set_mode((1280, 720))  # Configura a tela de exibição
    pygame.display.set_caption("Missão: Código Secreto - Fase 5")  # Título da janela

    # Tentativa de carregar uma fonte pixelada, se não carregar, usa uma fonte padrão
    try:
        pixel_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 32)
    except:
        pixel_font = pygame.font.SysFont("Courier", 32)

    # Definindo as dimensões do mundo
    WORLD_WIDTH, WORLD_HEIGHT = 2560, 1440
    player, player_speed = criar_jogador(WORLD_WIDTH, WORLD_HEIGHT)  # Criação do jogador
    jogador_carregando = None  # Inicializa o jogador que estará carregando uma resposta

    equacao = gerar_equacao_2_grau()  # Gera uma equação de 2º grau
    equacao["rect"] = pygame.Rect(random.randint(100, WORLD_WIDTH - 420),
                                  random.randint(100, WORLD_HEIGHT - 100), 320, 60)  # Define onde a equação aparecerá na tela

    respostas = []  # Lista para armazenar as respostas
    # Adiciona as respostas corretas à lista
    for resposta in equacao["respostas"]:
        respostas.append({
            "valor": resposta,
            "rect": pygame.Rect(random.randint(100, WORLD_WIDTH - 100),
                                random.randint(100, WORLD_HEIGHT - 100), 50, 50)
        })

    # Adiciona uma resposta errada à lista de respostas
    alternativa_errada = None
    while True:
        alt = random.randint(-10, 10)
        if alt not in equacao["respostas"]:
            alternativa_errada = alt
            break
    respostas.append({
        "valor": alternativa_errada,
        "rect": pygame.Rect(random.randint(100, WORLD_WIDTH - 100),
                            random.randint(100, WORLD_HEIGHT - 100), 50, 50)
    })

    # Define a porta de saída da fase
    porta = pygame.Rect(2400, 1200, 100, 100)
    porta_ativa = False  # A porta inicialmente não está ativa
    pontos = 0  # Inicializa os pontos
    respostas_corretas_coletadas = []  # Lista de respostas corretas já coletadas
    clock = pygame.time.Clock()  # Controla a taxa de atualização da tela

    # Loop principal do jogo
    while True:
        tela.fill((15, 15, 15))  # Preenche o fundo da tela com uma cor escura

        # Lida com os eventos do jogo, como fechar a janela ou apertar ESC para pausar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                acao_pause = pause_menu(tela, pixel_font, fase_numero=5)
                if acao_pause == "menu":
                    return "menu"  # Retorna ao menu se o jogo for pausado

        # Movimentação do jogador
        keys = pygame.key.get_pressed()
        player = mover_jogador(player, player_speed, keys, WORLD_WIDTH, WORLD_HEIGHT)
        coletar, dropar = checar_interacoes(keys)  # Verifica se o jogador está coletando ou droppando itens

        # Ajusta o deslocamento da tela conforme a posição do jogador
        offset_x = player.x - 1280 // 2 + player.width // 2
        offset_y = player.y - 720 // 2 + player.height // 2

        # Verifica se o jogador está carregando uma resposta
        if jogador_carregando is None:
            for resposta in respostas:
                if player.colliderect(resposta["rect"]) and coletar:
                    jogador_carregando = resposta
                    respostas.remove(resposta)
                    break

        # Verifica se o jogador está tentando dropar uma resposta
        if jogador_carregando and dropar:
            jogador_carregando["rect"].x = player.x + player.width // 2 - jogador_carregando["rect"].width // 2
            jogador_carregando["rect"].y = player.y + player.height // 2 - jogador_carregando["rect"].height // 2
            respostas.append(jogador_carregando)
            jogador_carregando = None

        # Verifica se o jogador está interagindo com a equação
        if jogador_carregando and not equacao["resolvida"]:
            if player.colliderect(equacao["rect"]):
                if jogador_carregando["valor"] in equacao["respostas"]:
                    if jogador_carregando["valor"] not in respostas_corretas_coletadas:
                        respostas_corretas_coletadas.append(jogador_carregando["valor"])
                        pontos += 1
                    if len(respostas_corretas_coletadas) == len(equacao["respostas"]):
                        equacao["resolvida"] = True  # Marca a equação como resolvida
                jogador_carregando = None

        # Se a equação foi resolvida, ativa a porta de saída
        if equacao["resolvida"]:
            porta_ativa = True

        # Define a cor da equação com base no progresso
        if equacao["resolvida"]:
            cor_eq = (0, 255, 0)  # Cor verde para equação resolvida
        elif len(respostas_corretas_coletadas) > 0:
            cor_eq = (255, 255, 0)  # Cor amarela para progresso
        else:
            cor_eq = (255, 100, 100)  # Cor vermelha para equação ainda não resolvida

        # Desenha a equação na tela
        rect_eq = equacao["rect"].copy()
        rect_eq.x -= offset_x
        rect_eq.y -= offset_y
        pygame.draw.rect(tela, cor_eq, rect_eq)
        texto_eq = pixel_font.render(equacao["pergunta"], True, (0, 0, 0))
        tela.blit(texto_eq, (rect_eq.x + 10, rect_eq.y + 15))

        # Desenha as respostas na tela
        for resposta in respostas:
            rect = resposta["rect"].copy()
            rect.x -= offset_x
            rect.y -= offset_y
            pygame.draw.rect(tela, (255, 255, 0), rect)
            texto = pixel_font.render(str(resposta["valor"]), True, (0, 0, 0))
            tela.blit(texto, (rect.x + 5, rect.y + 5))

        # Desenha o jogador na tela
        player_rect_tela = pygame.Rect(1280 // 2 - player.width // 2,
                                       720 // 2 - player.height // 2, player.width, player.height)
        pygame.draw.rect(tela, (0, 200, 255), player_rect_tela)

        # Exibe o item que o jogador está carregando, se houver
        if jogador_carregando:
            texto_item = pixel_font.render(f"Carregando: {jogador_carregando['valor']}", True, (255, 255, 255))
            tela.blit(texto_item, (20, 660))

        # Se a porta estiver ativa, desenha a porta de saída
        if porta_ativa:
            porta_rect_tela = porta.copy()
            porta_rect_tela.x -= offset_x
            porta_rect_tela.y -= offset_y
            pygame.draw.rect(tela, (0, 0, 255), porta_rect_tela)
            texto_porta = pixel_font.render("Fase Completa!", True, (0, 0, 0))
            tela.blit(texto_porta, (porta_rect_tela.x + 5, porta_rect_tela.y + 35))

            if player.colliderect(porta):
                # Chama a tela final e aguarda retorno
                resultado = tela_final(tela, pixel_font)
                return resultado  # Retorna o resultado da tela final

        # Exibe a pontuação na tela
        texto_pontos = pixel_font.render(f"Pontos: {pontos}", True, (255, 255, 255))
        tela.blit(texto_pontos, (1080, 20))

        # Atualiza a tela e controla a taxa de quadros por segundo
        pygame.display.flip()
        clock.tick(60)
