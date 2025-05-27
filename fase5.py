# === Importações ===
import pygame
import sys
import random
import math
from jogador import criar_jogador, mover_jogador, checar_interacoes
from pause_menu import pause_menu
from fim_de_jogo import tela_final
from game_over import game_over
from status_jogador import StatusJogador  # <-- Novo: importa a classe de status

# === Função para gerar uma equação de 2º grau com raízes inteiras ===
def gerar_equacao_2_grau():
    while True:
        a = random.randint(1, 3)
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        delta = b**2 - 4 * a * c
        if delta >= 0:
            x1 = (-b + math.sqrt(delta)) / (2 * a)
            x2 = (-b - math.sqrt(delta)) / (2 * a)
            if x1.is_integer() and x2.is_integer():
                pergunta = f"{a}x² + {b}x + {c} = 0"
                return {
                    "pergunta": pergunta,
                    "respostas": [int(x1), int(x2)],
                    "resolvida": False,
                    "rect": None
                }

# === Função principal da fase 5 ===
def fase5():
    pygame.init()
    tela = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Missão: Código Secreto - Fase 5")

    try:
        pixel_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 32)
    except:
        pixel_font = pygame.font.SysFont("Courier", 32)

    # Inicializa o status do jogador (vidas e pontos)
    status = StatusJogador()

    WORLD_WIDTH, WORLD_HEIGHT = 2560, 1440
    player, player_speed = criar_jogador(WORLD_WIDTH, WORLD_HEIGHT)
    jogador_carregando = None

    # Gera a equação do segundo grau
    equacao = gerar_equacao_2_grau()
    equacao["rect"] = pygame.Rect(random.randint(100, WORLD_WIDTH - 420),
                                   random.randint(100, WORLD_HEIGHT - 100), 320, 60)

    # Cria as respostas (duas corretas e uma errada)
    respostas = []
    for resposta in equacao["respostas"]:
        respostas.append({
            "valor": resposta,
            "rect": pygame.Rect(random.randint(100, WORLD_WIDTH - 100),
                                 random.randint(100, WORLD_HEIGHT - 100), 50, 50)
        })

    # Adiciona uma resposta errada
    while True:
        alt = random.randint(-10, 10)
        if alt not in equacao["respostas"]:
            respostas.append({
                "valor": alt,
                "rect": pygame.Rect(random.randint(100, WORLD_WIDTH - 100),
                                     random.randint(100, WORLD_HEIGHT - 100), 50, 50)
            })
            break

    porta = pygame.Rect(2400, 1200, 100, 100)
    porta_ativa = False

    respostas_corretas_coletadas = []
    clock = pygame.time.Clock()

    while True:
        tela.fill((15, 15, 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                acao_pause = pause_menu(tela, pixel_font, fase_numero=5)
                if acao_pause == "menu":
                    return "menu"

        keys = pygame.key.get_pressed()
        player = mover_jogador(player, player_speed, keys, WORLD_WIDTH, WORLD_HEIGHT)
        coletar, dropar = checar_interacoes(keys)

        offset_x = player.x - 1280 // 2 + player.width // 2
        offset_y = player.y - 720 // 2 + player.height // 2

        # Coleta de item
        if jogador_carregando is None:
            for resposta in respostas:
                if player.colliderect(resposta["rect"]) and coletar:
                    jogador_carregando = resposta
                    respostas.remove(resposta)
                    break

        # Dropar item
        if jogador_carregando and dropar:
            jogador_carregando["rect"].x = player.x + player.width // 2 - jogador_carregando["rect"].width // 2
            jogador_carregando["rect"].y = player.y + player.height // 2 - jogador_carregando["rect"].height // 2
            respostas.append(jogador_carregando)
            jogador_carregando = None

        # Interação com a equação
        if jogador_carregando and not equacao["resolvida"]:
            if player.colliderect(equacao["rect"]):
                if jogador_carregando["valor"] in equacao["respostas"]:
                    if jogador_carregando["valor"] not in respostas_corretas_coletadas:
                        respostas_corretas_coletadas.append(jogador_carregando["valor"])
                        status.ganhar_pontos(100)  # <-- Novo: ganhar pontos

                    if len(respostas_corretas_coletadas) == len(equacao["respostas"]):
                        equacao["resolvida"] = True
                        status.ganhar_pontos(900) 
                else:
                    status.perder_vida()  # <-- Novo: perde vida ao errar
                    if status.game_over():  # <-- Novo: verifica fim de jogo
                        acao = game_over(tela, pixel_font)
                        if acao == "reiniciar":
                            return fase5()
                        elif acao == "sair":
                            return "menu"

                jogador_carregando = None

        if equacao["resolvida"]:
            porta_ativa = True

        if equacao["resolvida"]:
            cor_eq = (0, 255, 0)  # Verde
        elif len(respostas_corretas_coletadas) > 0:
            cor_eq = (255, 255, 0)  # Amarelo
        else:
            cor_eq = (255, 100, 100)  # Vermelho

        rect_eq = equacao["rect"].copy()
        rect_eq.x -= offset_x
        rect_eq.y -= offset_y
        pygame.draw.rect(tela, cor_eq, rect_eq)
        texto_eq = pixel_font.render(equacao["pergunta"], True, (0, 0, 0))
        tela.blit(texto_eq, (rect_eq.x + 10, rect_eq.y + 15))

        for resposta in respostas:
            rect = resposta["rect"].copy()
            rect.x -= offset_x
            rect.y -= offset_y
            pygame.draw.rect(tela, (255, 255, 0), rect)
            texto = pixel_font.render(str(resposta["valor"]), True, (0, 0, 0))
            tela.blit(texto, (rect.x + 5, rect.y + 5))

        player_rect_tela = pygame.Rect(1280 // 2 - player.width // 2, 720 // 2 - player.height // 2, player.width, player.height)
        pygame.draw.rect(tela, (0, 200, 255), player_rect_tela)

        if jogador_carregando:
            texto_item = pixel_font.render(f"Carregando: {jogador_carregando['valor']}", True, (255, 255, 255))
            tela.blit(texto_item, (20, 660))

        if porta_ativa:
            porta_rect_tela = porta.copy()
            porta_rect_tela.x -= offset_x
            porta_rect_tela.y -= offset_y
            pygame.draw.rect(tela, (0, 0, 255), porta_rect_tela)
            texto_porta = pixel_font.render("Fase Completa!", True, (0, 0, 0))
            tela.blit(texto_porta, (porta_rect_tela.x + 5, porta_rect_tela.y + 35))

            if player.colliderect(porta):
                resultado = tela_final(tela, pixel_font)
                return resultado

        # Novo: exibe vidas e pontos
        status.renderizar(tela, pixel_font)

        pygame.display.flip()
        clock.tick(60)