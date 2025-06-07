import pygame
import sys
import random
from jogador import Jogador
from pause_menu import pause_menu
from status_jogador import StatusJogador
from game_over import game_over
from fase5 import fase5

def gerar_equacao_1_grau():
    a = random.randint(1, 10)
    b = random.randint(1, 20)
    x = random.randint(1, 10)
    resultado = a * x + b
    pergunta = f"{a}x + {b} = {resultado}"
    resposta = x
    return {"pergunta": pergunta, "resposta": resposta}

class MiniMapaF4:
    def __init__(self, world_width, world_height, pos=(1060, 10), size=(200, 112)):
        self.world_width = world_width
        self.world_height = world_height
        self.pos = pos
        self.width, self.height = size
        self.escala_x = self.width / self.world_width
        self.escala_y = self.height / self.world_height

    def converter_para_minimapa(self, rect):
        return pygame.Rect(
            self.pos[0] + int(rect.x * self.escala_x),
            self.pos[1] + int(rect.y * self.escala_y),
            max(2, int(rect.width * self.escala_x)),
            max(2, int(rect.height * self.escala_y))
        )

    def desenhar(self, tela, jogador_rect, equacoes, respostas, porta, cor_eq=(255, 100, 100), porta_ativa=True):
        pygame.draw.rect(tela, (50, 50, 50), (self.pos[0] - 2, self.pos[1] - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(tela, (20, 20, 20), (self.pos[0], self.pos[1], self.width, self.height))

        pygame.draw.rect(tela, (0, 255, 255), self.converter_para_minimapa(jogador_rect))

        for eq in equacoes:
            pygame.draw.rect(tela, cor_eq, self.converter_para_minimapa(eq["rect"]))

        for resp in respostas:
            pygame.draw.rect(tela, (255, 255, 0), self.converter_para_minimapa(resp["rect"]))

        if porta_ativa:
            pygame.draw.rect(tela, (0, 0, 255), self.converter_para_minimapa(porta))

def fase4():
    pygame.init()
    tela = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Missão: Código Secreto - Fase 4")

    try:
        pixel_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 32)
    except:
        pixel_font = pygame.font.SysFont("Courier", 32)

    WORLD_WIDTH, WORLD_HEIGHT = 2560, 1440
    minimapa = MiniMapaF4(WORLD_WIDTH, WORLD_HEIGHT)

    jogador = Jogador(WORLD_WIDTH, WORLD_HEIGHT)
    status = StatusJogador()
    jogador_carregando = None

    porta = pygame.Rect(2400, 1300, 100, 100)
    porta_ativa = False

    # Criar equação com retângulo
    eq = gerar_equacao_1_grau()
    equacoes = [{
        "texto": eq["pergunta"],
        "resposta": eq["resposta"],
        "rect": pygame.Rect(500, 300, 300, 60),
        "resolvida": False
    }]

    # Criar respostas
    respostas = []
    for i in range(4):
        valor = eq["resposta"] if i == 0 else random.randint(1, 20)
        respostas.append({
            "valor": valor,
            "rect": pygame.Rect(random.randint(100, WORLD_WIDTH - 100), random.randint(100, WORLD_HEIGHT - 100), 50, 50)
        })

    clock = pygame.time.Clock()

    while True:
        tela.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    acao = pause_menu(tela, pixel_font, 4)
                    if acao == "menu":
                        return "menu"

        keys = pygame.key.get_pressed()
        jogador.update(keys, WORLD_WIDTH, WORLD_HEIGHT)
        coletar, dropar = jogador.checar_interacoes(keys)

        offset_x = jogador.rect.x - 1280 // 2 + jogador.rect.width // 2
        offset_y = jogador.rect.y - 720 // 2 + jogador.rect.height // 2

        # --- Coleta de item ---
        if jogador_carregando is None:
            for resposta in respostas:
                if jogador.hitbox.colliderect(resposta["rect"]) and coletar:
                    jogador_carregando = resposta
                    respostas.remove(resposta)
                    break

        # --- Drop do item ---
        if jogador_carregando and dropar:
            jogador_carregando["rect"].x = jogador.rect.x + jogador.rect.width // 2 - jogador_carregando["rect"].width // 2
            jogador_carregando["rect"].y = jogador.rect.y + jogador.rect.height // 2 - jogador_carregando["rect"].height // 2
            respostas.append(jogador_carregando)
            jogador_carregando = None

        # --- Verifica se item foi colocado na equação correta ---
        if jogador_carregando:
            for eq in equacoes:
                if jogador.hitbox.colliderect(eq["rect"]) and not eq["resolvida"]:
                    if jogador_carregando["valor"] == eq["resposta"]:
                        status.ganhar_pontos(100)
                        eq["resolvida"] = True
                        porta_ativa = True
                    else:
                        status.perder_vida()
                        if status.game_over():
                            return game_over(tela, pixel_font)
                    jogador_carregando = None

        # --- Desenhar equações ---
        for eq in equacoes:
            cor = (0, 255, 0) if eq["resolvida"] else (255, 100, 100)
            rect = eq["rect"].copy()
            rect.x -= offset_x
            rect.y -= offset_y
            pygame.draw.rect(tela, cor, rect)
            texto_eq = pixel_font.render(eq["texto"], True, (0, 0, 0))
            tela.blit(texto_eq, (rect.x + 10, rect.y + 15))

        # --- Desenhar respostas ---
        for resposta in respostas:
            rect = resposta["rect"].copy()
            rect.x -= offset_x
            rect.y -= offset_y
            pygame.draw.rect(tela, (255, 255, 0), rect)
            texto = pixel_font.render(str(resposta["valor"]), True, (0, 0, 0))
            tela.blit(texto, (rect.x + 5, rect.y + 5))

        # --- Desenhar jogador ---
        jogador_tela_rect = jogador.rect.copy()
        jogador_tela_rect.x -= offset_x
        jogador_tela_rect.y -= offset_y
        tela.blit(jogador.image, jogador_tela_rect)

        # Mostrar item carregado
        if jogador_carregando:
            texto_item = pixel_font.render(
                f"Carregando: {round(jogador_carregando['valor'], 2)}",
                True, (255, 255, 255)
            )
            tela.blit(texto_item, (20, 660))

        # --- Desenhar porta ---
        if porta_ativa:
            porta_rect_tela = porta.copy()
            porta_rect_tela.x -= offset_x
            porta_rect_tela.y -= offset_y
            pygame.draw.rect(tela, (0, 0, 255), porta_rect_tela)
            texto_porta = pixel_font.render("Ir para fase 5", True, (255, 255, 255))
            tela.blit(texto_porta, (porta_rect_tela.x, porta_rect_tela.y - 30))

        # Avançar para próxima fase
        if porta_ativa and jogador.rect.colliderect(porta):
            return fase5()

        minimapa.desenhar(tela, jogador.rect, equacoes, respostas, porta, porta_ativa=porta_ativa)
        status.renderizar(tela, pixel_font)

        pygame.display.flip()
        clock.tick(60)


