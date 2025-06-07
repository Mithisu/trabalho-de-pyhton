import pygame
import sys
import random
from jogador import Jogador  # Importa a classe Jogador
from fase2 import fase2  # Importa a próxima fase
from pause_menu import pause_menu  # Importa a tela de pause 
from game_over import game_over   
from status_jogador import StatusJogador  # Importa a classe de status

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

    try:
        pixel_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 32)
    except:
        pixel_font = pygame.font.SysFont("Courier", 32)

    WORLD_WIDTH = 2560
    WORLD_HEIGHT = 1440

    status = StatusJogador()
    jogador = Jogador(WORLD_WIDTH, WORLD_HEIGHT)  
    jogador_carregando = None  

    # Gera as equações da fase
    equacoes = [
        gerar_equacao_soma(),
        gerar_equacao_subtracao(),
        gerar_equacao_multiplicacao(),
        gerar_equacao_divisao(),
    ]

    # Define posição de cada equação no mapa
    for eq in equacoes:
        eq["rect"] = pygame.Rect(random.randint(100, WORLD_WIDTH - 260),
                                 random.randint(100, WORLD_HEIGHT - 160), 160, 60)
        eq["resolvida"] = False

    respostas = []

    # Cria alternativas (uma correta e uma errada) para cada equação
    for eq in equacoes:
        respostas.append({
            "valor": eq["resposta"],
            "rect": pygame.Rect(random.randint(100, WORLD_WIDTH - 70),
                                random.randint(100, WORLD_HEIGHT - 70), 50, 50)
        })
        valor_errado = gerar_alternativa_errada(eq["resposta"], minimo=0, maximo=100)
        respostas.append({
            "valor": valor_errado,
            "rect": pygame.Rect(random.randint(100, WORLD_WIDTH - 70),
                                random.randint(100, WORLD_HEIGHT - 70), 50, 50)
        })

    porta = pygame.Rect(2400, 1200, 100, 100)  
    porta_ativa = False  

    clock = pygame.time.Clock()

    # Configurações do minimapa
    MINIMAPA_WIDTH = 200
    MINIMAPA_HEIGHT = 112
    MINIMAPA_POS = (1060, 10)  # canto superior direito
    ESCALA_X = MINIMAPA_WIDTH / WORLD_WIDTH
    ESCALA_Y = MINIMAPA_HEIGHT / WORLD_HEIGHT

    def converter_para_minimapa(rect):
        return pygame.Rect(
            MINIMAPA_POS[0] + int(rect.x * ESCALA_X),
            MINIMAPA_POS[1] + int(rect.y * ESCALA_Y),
            max(2, int(rect.width * ESCALA_X)),
            max(2, int(rect.height * ESCALA_Y))
        )

    running = True
    while running:
        tela.fill((255, 255, 255))  # Fundo branco

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                acao_pause = pause_menu(tela, pixel_font, fase_numero=1)
                if acao_pause == "menu":
                    return "menu"

        keys = pygame.key.get_pressed()
        jogador.update(keys, WORLD_WIDTH, WORLD_HEIGHT)
        coletar, dropar = jogador.checar_interacoes(keys)

        offset_x = jogador.rect.x - 1280 // 2 + jogador.rect.width // 2
        offset_y = jogador.rect.y - 720 // 2 + jogador.rect.height // 2

        # Limita offset para não mostrar área fora do mapa
        offset_x = max(0, min(offset_x, WORLD_WIDTH - 1280))
        offset_y = max(0, min(offset_y, WORLD_HEIGHT - 720))

        # Pegar item
        if jogador_carregando is None:
            for resposta in respostas:
                if jogador.hitbox.colliderect(resposta["rect"]) and coletar:
                    jogador_carregando = resposta
                    respostas.remove(resposta)
                    break

        # Soltar item
        if jogador_carregando and dropar:
            jogador_carregando["rect"].x = jogador.rect.x + jogador.rect.width // 2 - jogador_carregando["rect"].width // 2
            jogador_carregando["rect"].y = jogador.rect.y + jogador.rect.height // 2 - jogador_carregando["rect"].height // 2
            respostas.append(jogador_carregando)
            jogador_carregando = None

        # Tentar entregar resposta
        if jogador_carregando:
            for eq in equacoes:
                if jogador.hitbox.colliderect(eq["rect"]) and not eq["resolvida"]:
                    if jogador_carregando["valor"] == eq["resposta"]:
                        status.ganhar_pontos(100)
                        eq["resolvida"] = True
                        status.ganhar_pontos(150)
                        jogador_carregando = None
                    else:
                        status.perder_vida()
                        jogador_carregando = None
                        if status.game_over():
                            acao = game_over(tela, pixel_font)
                            if acao == "reiniciar":
                                return fase1()
                            elif acao == "sair":
                                return "menu"

        # Desenho das equações
        for eq in equacoes:
            cor = (0, 255, 0) if eq["resolvida"] else (255, 100, 100)
            rect = eq["rect"].copy()
            rect.x -= offset_x
            rect.y -= offset_y
            pygame.draw.rect(tela, cor, rect)
            texto = pixel_font.render(eq["pergunta"], True, (0, 0, 0))
            tela.blit(texto, (rect.x + 10, rect.y + 15))

        # Desenho das respostas
        for resposta in respostas:
            rect = resposta["rect"].copy()
            rect.x -= offset_x
            rect.y -= offset_y
            pygame.draw.rect(tela, (255, 255, 0), rect)
            texto = pixel_font.render(str(resposta["valor"]), True, (0, 0, 0))
            tela.blit(texto, (rect.x + 5, rect.y + 5))

        # Desenha jogador
        jogador_tela_rect = jogador.rect.copy()
        jogador_tela_rect.x -= offset_x
        jogador_tela_rect.y -= offset_y
        tela.blit(jogador.image, jogador_tela_rect)

        # Exibe valor carregado
        if jogador_carregando:
            texto_item = pixel_font.render(f"Carregando: {jogador_carregando['valor']}", True, (100, 100, 100))
            tela.blit(texto_item, (20, 660))

        # Ativa porta quando todas as equações forem resolvidas
        if all(eq["resolvida"] for eq in equacoes):
            porta_ativa = True

        # Desenha porta (se ativa)
        if porta_ativa:
            porta_rect_tela = porta.copy()
            porta_rect_tela.x -= offset_x
            porta_rect_tela.y -= offset_y
            pygame.draw.rect(tela, (0, 0, 255), porta_rect_tela)
            texto_porta = pixel_font.render("Ir para próxima fase", True, (0, 0, 0))
            tela.blit(texto_porta, (porta_rect_tela.x + 10, porta_rect_tela.y + 35))

        # Verifica se jogador entrou na porta para ir pra fase 2
        if porta_ativa and jogador.rect.colliderect(porta):
            retorno = fase2()
            if retorno == "menu":
                return "menu"

        # Desenha minimapa
        pygame.draw.rect(tela, (50, 50, 50), (MINIMAPA_POS[0] - 2, MINIMAPA_POS[1] - 2, MINIMAPA_WIDTH + 4, MINIMAPA_HEIGHT + 4))  # Borda
        pygame.draw.rect(tela, (20, 20, 20), (MINIMAPA_POS[0], MINIMAPA_POS[1], MINIMAPA_WIDTH, MINIMAPA_HEIGHT))  # Fundo

        # Jogador no minimapa
        pygame.draw.rect(tela, (0, 255, 255), converter_para_minimapa(jogador.rect))

        # Equações no minimapa
        for eq in equacoes:
            cor = (0, 255, 0) if eq["resolvida"] else (255, 0, 0)
            pygame.draw.rect(tela, cor, converter_para_minimapa(eq["rect"]))

        # Respostas no minimapa
        for resposta in respostas:
            pygame.draw.rect(tela, (255, 255, 0), converter_para_minimapa(resposta["rect"]))

        # Porta no minimapa
        if porta_ativa:
            pygame.draw.rect(tela, (0, 0, 255), converter_para_minimapa(porta))

        # Mostra vidas e pontos
        status.renderizar(tela, pixel_font)

        pygame.display.flip()
        clock.tick(60)
