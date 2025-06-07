import pygame
import sys
import random
from jogador import Jogador
from pause_menu import pause_menu
from status_jogador import StatusJogador
from game_over import game_over

def gerar_equacao_2_grau():
    a = random.randint(1, 5)
    b = random.randint(1, 10)
    c = random.randint(1, 10)
    pergunta = f"{a}x² + {b}x + {c} = 0"
    resposta = random.choice([1, -1, 2])  # dummy
    return {"pergunta": pergunta, "resposta": resposta}

class MiniMapaF5:
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

    def desenhar(self, tela, jogador_rect, equacoes, respostas, porta, mostrar_porta=False, cor_eq=(255, 50, 50)):
        pygame.draw.rect(tela, (60, 60, 60), (self.pos[0] - 2, self.pos[1] - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(tela, (30, 30, 30), (self.pos[0], self.pos[1], self.width, self.height))

        pygame.draw.rect(tela, (0, 255, 255), self.converter_para_minimapa(jogador_rect))

        for eq in equacoes:
            pygame.draw.rect(tela, cor_eq, self.converter_para_minimapa(eq["rect"]))

        for resp in respostas:
            pygame.draw.rect(tela, (255, 255, 0), self.converter_para_minimapa(resp["rect"]))

        if mostrar_porta:
            pygame.draw.rect(tela, (0, 0, 255), self.converter_para_minimapa(porta))


def fase5():
    pygame.init()
    tela = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Missão: Código Secreto - Fase 5")
    try:
        pixel_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 32)
    except:
        pixel_font = pygame.font.SysFont("Courier", 32)

    WORLD_WIDTH, WORLD_HEIGHT = 2560, 1440
    minimapa = MiniMapaF5(WORLD_WIDTH, WORLD_HEIGHT)

    jogador = Jogador(WORLD_WIDTH, WORLD_HEIGHT)
    status = StatusJogador()

    porta = pygame.Rect(2400, 1300, 100, 100)

    eq = gerar_equacao_2_grau()
    equacoes = [{"texto": eq["pergunta"], "resposta": eq["resposta"], "rect": pygame.Rect(400, 300, 130, 50)}]

    respostas = []
    # Gerar 3 respostas, uma correta e duas erradas em posições aleatórias
    for i in range(3):
        x = random.randint(300, 2200)
        y = random.randint(300, 1100)
        valor = eq["resposta"] if i == 0 else random.randint(-5, 5)
        respostas.append({"valor": valor, "rect": pygame.Rect(x, y, 80, 50)})

    porta_ativa = False  # Porta começa invisível

    clock = pygame.time.Clock()

    while True:
        tela.fill((60, 60, 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    acao = pause_menu(tela, pixel_font, 5)
                    if acao == "menu":
                        return "menu"

        keys = pygame.key.get_pressed()
        jogador.update(keys, WORLD_WIDTH, WORLD_HEIGHT)

        offset_x = jogador.rect.x - 1280 // 2 + jogador.rect.width // 2
        offset_y = jogador.rect.y - 720 // 2 + jogador.rect.height // 2

        # Desenhar equação fixa
        eq_pos = (400 - offset_x, 300 - offset_y)
        eq_rect = pygame.Rect(eq_pos[0], eq_pos[1], 130, 50)
        pygame.draw.rect(tela, (255, 50, 50), eq_rect)
        texto_eq = pixel_font.render(eq["pergunta"], True, (255, 255, 255))
        tela.blit(texto_eq, (eq_pos[0], eq_pos[1]))

        # Desenhar respostas na tela e verificar colisão para coleta
        for resp in respostas[:]:  # iterar em cópia para poder remover
            resp_tela_rect = resp["rect"].copy()
            resp_tela_rect.x -= offset_x
            resp_tela_rect.y -= offset_y

            pygame.draw.rect(tela, (255, 255, 0), resp_tela_rect)
            texto_resp = pixel_font.render(str(resp["valor"]), True, (0, 0, 0))
            tela.blit(texto_resp, (resp_tela_rect.x + 10, resp_tela_rect.y + 10))

            # Detectar colisão com jogador para coletar resposta
            if jogador.rect.colliderect(resp["rect"]):
                if resp["valor"] == eq["resposta"]:
                    status.ganhar_pontos(15)
                    respostas.remove(resp)
                    # Se não tem mais respostas corretas no mapa, ativar porta
                    if not any(r["valor"] == eq["resposta"] for r in respostas):
                        porta_ativa = True
                else:
                    status.perder_vida()
                    respostas.remove(resp)
                    if status.game_over():
                        return game_over(tela, pixel_font)

        # Desenhar jogador
        jogador_tela = jogador.rect.copy()
        jogador_tela.x -= offset_x
        jogador_tela.y -= offset_y
        tela.blit(jogador.image, jogador_tela)

        # Desenhar porta só se ativada
        if porta_ativa:
            porta_tela = porta.copy()
            porta_tela.x -= offset_x
            porta_tela.y -= offset_y
            pygame.draw.rect(tela, (0, 0, 255), porta_tela)
            texto_porta = pixel_font.render("Porta", True, (255, 255, 255))
            tela.blit(texto_porta, (porta_tela.x, porta_tela.y - 30))

            # Detectar colisão do jogador com porta para vitória
            if jogador.rect.colliderect(porta):
                return "vitoria"  # Ou próxima fase

        minimapa.desenhar(tela, jogador.rect, equacoes=equacoes, respostas=respostas, porta=porta, mostrar_porta=porta_ativa)

        status.renderizar(tela, pixel_font)

        pygame.display.flip()
        clock.tick(60)
