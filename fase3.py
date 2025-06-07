import pygame
import random
import sys
from jogador import Jogador
from fase4 import fase4
from pause_menu import pause_menu
from game_over import game_over
from status_jogador import StatusJogador

def gerar_equacao_porcentagem():
    porcentagem = random.randint(1, 50)
    valor = random.randint(10, 200)
    resultado = (porcentagem / 100) * valor
    pergunta = f"{porcentagem}% de {valor}"
    resposta = round(resultado, 2)
    return {"pergunta": pergunta, "resposta": resposta}

def gerar_equacao_regra_de_3():
    a = random.randint(1, 50)
    b = random.randint(1, 50)
    c = random.randint(1, 50)
    resultado = (b * c) / a
    pergunta = f"{a} está para {b} como {c} está para x"
    resposta = round(resultado, 2)
    return {"pergunta": pergunta, "resposta": resposta}

def fase3():
    pygame.init()
    tela = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Missão: Código Secreto - Fase 3")

    try:
        pixel_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 32)
    except:
        pixel_font = pygame.font.SysFont("Courier", 32)

    WORLD_WIDTH = 2560
    WORLD_HEIGHT = 1440

    # Configurações do minimapa
    MINIMAPA_WIDTH = 200
    MINIMAPA_HEIGHT = 112
    MINIMAPA_POS = (1060, 10)
    ESCALA_X = MINIMAPA_WIDTH / WORLD_WIDTH
    ESCALA_Y = MINIMAPA_HEIGHT / WORLD_HEIGHT

    def converter_para_minimapa(rect):
        return pygame.Rect(
            MINIMAPA_POS[0] + int(rect.x * ESCALA_X),
            MINIMAPA_POS[1] + int(rect.y * ESCALA_Y),
            max(2, int(rect.width * ESCALA_X)),
            max(2, int(rect.height * ESCALA_Y))
        )

    jogador = Jogador(WORLD_WIDTH, WORLD_HEIGHT)
    jogador_carregando = None
    status = StatusJogador()

    equacoes = [gerar_equacao_porcentagem(), gerar_equacao_regra_de_3()]
    for eq in equacoes:
        eq["rect"] = pygame.Rect(
            random.randint(100, WORLD_WIDTH - 100),
            random.randint(100, WORLD_HEIGHT - 100),
            300, 60
        )
        eq["resolvida"] = False

    respostas = []
    for eq in equacoes:
        respostas.append({
            "valor": eq["resposta"],
            "rect": pygame.Rect(
                random.randint(100, WORLD_WIDTH - 100),
                random.randint(100, WORLD_HEIGHT - 100),
                50, 50
            )
        })

    alternativas_erradas = set()
    while len(alternativas_erradas) < 4:
        alt_errada = round(random.uniform(1, 200), 2)
        if alt_errada not in [r["valor"] for r in respostas]:
            alternativas_erradas.add(alt_errada)

    for alt in alternativas_erradas:
        respostas.append({
            "valor": alt,
            "rect": pygame.Rect(
                random.randint(100, WORLD_WIDTH - 100),
                random.randint(100, WORLD_HEIGHT - 100),
                50, 50
            )
        })

    porta = pygame.Rect(2400, 1200, 100, 100)
    porta_ativa = False

    clock = pygame.time.Clock()
    running = True

    while running:
        tela.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                acao_pause = pause_menu(tela, pixel_font, fase_atual=3)
                if acao_pause == "menu":
                    return "menu"

        keys = pygame.key.get_pressed()
        jogador.update(keys, WORLD_WIDTH, WORLD_HEIGHT)
        coletar, dropar = jogador.checar_interacoes(keys)

        offset_x = jogador.rect.x - 1280 // 2 + jogador.rect.width // 2
        offset_y = jogador.rect.y - 720 // 2 + jogador.rect.height // 2

        if jogador_carregando is None:
            for resposta in respostas:
                if jogador.hitbox.colliderect(resposta["rect"]) and coletar:
                    jogador_carregando = resposta
                    respostas.remove(resposta)
                    break

        if jogador_carregando and dropar:
            jogador_carregando["rect"].x = jogador.rect.x + jogador.rect.width // 2 - jogador_carregando["rect"].width // 2
            jogador_carregando["rect"].y = jogador.rect.y + jogador.rect.height // 2 - jogador_carregando["rect"].height // 2
            respostas.append(jogador_carregando)
            jogador_carregando = None

        if jogador_carregando:
            for eq in equacoes:
                if jogador.hitbox.colliderect(eq["rect"]) and not eq["resolvida"]:
                    if round(jogador_carregando["valor"], 2) == round(eq["resposta"], 2):
                        status.ganhar_pontos(100)
                        eq["resolvida"] = True
                        status.ganhar_pontos(400)
                    else:
                        status.perder_vida()
                        if status.game_over():
                            acao = game_over(tela, pixel_font)
                            if acao == "reiniciar":
                                return fase3()
                            elif acao == "sair":
                                return "menu"
                    jogador_carregando = None

        # Desenhar equações
        for eq in equacoes:
            cor = (0, 255, 0) if eq["resolvida"] else (255, 100, 100)
            rect = eq["rect"].copy()
            rect.x -= offset_x
            rect.y -= offset_y
            pygame.draw.rect(tela, cor, rect)
            texto = pixel_font.render(eq["pergunta"], True, (0, 0, 0))
            tela.blit(texto, (rect.x + 10, rect.y + 15))

        # Desenhar respostas
        for resposta in respostas:
            rect = resposta["rect"].copy()
            rect.x -= offset_x
            rect.y -= offset_y
            pygame.draw.rect(tela, (255, 255, 0), rect)
            texto = pixel_font.render(str(resposta["valor"]), True, (0, 0, 0))
            tela.blit(texto, (rect.x + 5, rect.y + 5))

        # Desenhar jogador
        jogador_tela_rect = jogador.rect.copy()
        jogador_tela_rect.x -= offset_x
        jogador_tela_rect.y -= offset_y
        tela.blit(jogador.image, jogador_tela_rect)

        # Mostrar item carregado
        if jogador_carregando:
            texto_item = pixel_font.render(
                f"Carregando: {round(jogador_carregando['valor'], 2)}",
                True,
                (255, 255, 255)
            )
            tela.blit(texto_item, (20, 660))

        # Verifica se todas as equações foram resolvidas
        if all(eq["resolvida"] for eq in equacoes):
            porta_ativa = True

        # Desenha porta
        if porta_ativa:
            porta_rect_tela = porta.copy()
            porta_rect_tela.x -= offset_x
            porta_rect_tela.y -= offset_y
            pygame.draw.rect(tela, (0, 0, 255), porta_rect_tela)
            texto_porta = pixel_font.render("Ir para próxima fase", True, (0, 0, 0))
            tela.blit(texto_porta, (porta_rect_tela.x + 10, porta_rect_tela.y + 35))

        # Verifica se jogador entrou na porta
        if porta_ativa and jogador.rect.colliderect(porta):
            return fase4()

        status.renderizar(tela, pixel_font)

        # --- MINIMAPA ---
        pygame.draw.rect(tela, (50, 50, 50), (MINIMAPA_POS[0]-2, MINIMAPA_POS[1]-2, MINIMAPA_WIDTH+4, MINIMAPA_HEIGHT+4))  # borda
        pygame.draw.rect(tela, (20, 20, 20), (MINIMAPA_POS[0], MINIMAPA_POS[1], MINIMAPA_WIDTH, MINIMAPA_HEIGHT))  # fundo

        # Jogador no minimapa
        pygame.draw.rect(tela, (0, 255, 255), converter_para_minimapa(jogador.rect))

        # Equações no minimapa
        for eq in equacoes:
            cor = (0, 255, 0) if eq["resolvida"] else (255, 0, 0)
            pygame.draw.rect(tela, cor, converter_para_minimapa(eq["rect"]))

        # Respostas no minimapa
        for resposta in respostas:
            pygame.draw.rect(tela, (255, 255, 0), converter_para_minimapa(resposta["rect"]))

        pygame.display.flip()
        clock.tick(60)
