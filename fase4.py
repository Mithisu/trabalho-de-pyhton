import pygame
import sys
import random
from jogador import criar_jogador, mover_jogador, checar_interacoes
from fase5 import fase5
from pause_menu import pause_menu 

# Função que gera uma equação de 1º grau no formato "ax + b = resultado"
def gerar_equacao_1_grau():
    a = random.randint(1, 10)  # Coeficiente a entre 1 e 10
    b = random.randint(1, 20)  # Coeficiente b entre 1 e 20
    x = random.randint(1, 10)  # Valor de x entre 1 e 10
    resultado = a * x + b      # Resultado da equação
    pergunta = f"{a}x + {b} = {resultado}"  # Formatação da equação
    resposta = x               # Resposta correta para a equação
    return {"pergunta": pergunta, "resposta": resposta}

# Função principal da fase 4
def fase4():
    pygame.init()
    tela = pygame.display.set_mode((1280, 720))  # Definindo a tela do jogo com resolução 1280x720
    pygame.display.set_caption("Missão: Código Secreto - Fase 4")

    try:
        pixel_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 32)  # Tentativa de carregar uma fonte pixelada
    except:
        pixel_font = pygame.font.SysFont("Courier", 32)  # Se falhar, usa a fonte padrão Courier

    WORLD_WIDTH, WORLD_HEIGHT = 2560, 1440  # Dimensões do mundo
    player, player_speed = criar_jogador(WORLD_WIDTH, WORLD_HEIGHT)  # Criar jogador e sua velocidade
    jogador_carregando = None  # Variável que armazena o item que o jogador está carregando

    equacao = gerar_equacao_1_grau()  # Gerar uma equação
    equacao["rect"] = pygame.Rect(random.randint(100, WORLD_WIDTH - 100),
                                  random.randint(100, WORLD_HEIGHT - 100), 300, 60)  # Definir a área da equação na tela
    equacao["resolvida"] = False  # A equação ainda não foi resolvida

    # Respostas possíveis (uma correta e outras erradas)
    respostas = [{
        "valor": equacao["resposta"],
        "rect": pygame.Rect(random.randint(100, WORLD_WIDTH - 100),
                            random.randint(100, WORLD_HEIGHT - 100), 50, 50)
    }]

    # Gerar alternativas erradas
    alternativas_erradas = set()
    while len(alternativas_erradas) < 3:
        alt = random.randint(0, 20)
        if alt != equacao["resposta"]:
            alternativas_erradas.add(alt)

    # Adicionar as alternativas erradas à lista de respostas
    for alt in alternativas_erradas:
        respostas.append({
            "valor": alt,
            "rect": pygame.Rect(random.randint(100, WORLD_WIDTH - 100),
                                random.randint(100, WORLD_HEIGHT - 100), 50, 50)
        })

    porta = pygame.Rect(2400, 1200, 100, 100)  # Definir a posição e tamanho da porta de saída
    porta_ativa = False  # Inicialmente, a porta não está ativa
    pontos = 0  # Inicializa os pontos
    clock = pygame.time.Clock()  # Controlar a taxa de atualização do jogo

    while True:
        tela.fill((20, 20, 20))  # Preencher a tela com uma cor de fundo escura

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Se o jogador fechar a janela
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Se pressionar a tecla ESC, abre o menu de pausa
                fase_atual = 4
                acao_pause = pause_menu(tela, pixel_font, fase_atual)
                if acao_pause == "menu":
                    return "menu"  # Sai da fase para voltar ao menu principal

        keys = pygame.key.get_pressed()  # Obtém os teclados pressionados
        player = mover_jogador(player, player_speed, keys, WORLD_WIDTH, WORLD_HEIGHT)  # Atualiza a posição do jogador
        coletar, dropar = checar_interacoes(keys)  # Checa se o jogador está coletando ou dropando um item

        # Movimentação da tela (câmera segue o jogador)
        offset_x = player.x - 1280 // 2 + player.width // 2
        offset_y = player.y - 720 // 2 + player.height // 2

        # Verifica se o jogador está coletando um item de resposta
        if jogador_carregando is None:
            for resposta in respostas:
                if player.colliderect(resposta["rect"]) and coletar:
                    jogador_carregando = resposta
                    respostas.remove(resposta)
                    break

        # Se o jogador estiver carregando um item e pressionar a tecla para dropar
        if jogador_carregando and dropar:
            jogador_carregando["rect"].x = player.x + player.width // 2 - jogador_carregando["rect"].width // 2
            jogador_carregando["rect"].y = player.y + player.height // 2 - jogador_carregando["rect"].height // 2
            respostas.append(jogador_carregando)
            jogador_carregando = None

        # Verifica se o jogador resolveu a equação
        if jogador_carregando and not equacao["resolvida"]:
            if player.colliderect(equacao["rect"]):
                if jogador_carregando["valor"] == equacao["resposta"]:
                    pontos += 1  # Se acertar a resposta, ganha pontos
                    equacao["resolvida"] = True
                jogador_carregando = None

        # Define a cor da equação, dependendo se foi resolvida ou não
        cor_eq = (0, 255, 0) if equacao["resolvida"] else (255, 100, 100)
        rect_eq = equacao["rect"].copy()
        rect_eq.x -= offset_x
        rect_eq.y -= offset_y
        pygame.draw.rect(tela, cor_eq, rect_eq)
        texto_eq = pixel_font.render(equacao["pergunta"], True, (0, 0, 0))
        tela.blit(texto_eq, (rect_eq.x + 10, rect_eq.y + 15))

        # Desenha as alternativas de resposta
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

        # Se o jogador estiver carregando um item, exibe o nome do item
        if jogador_carregando:
            texto_item = pixel_font.render(f"Carregando: {jogador_carregando['valor']}", True, (255, 255, 255))
            tela.blit(texto_item, (20, 660))

        # Se a equação foi resolvida, ativa a porta
        if equacao["resolvida"]:
            porta_ativa = True

        # Se a porta estiver ativa, desenha e verifica se o jogador a tocou
        if porta_ativa:
            porta_rect_tela = porta.copy()
            porta_rect_tela.x -= offset_x
            porta_rect_tela.y -= offset_y
            pygame.draw.rect(tela, (0, 0, 255), porta_rect_tela)
            texto_porta = pixel_font.render("Ir para próxima fase", True, (0, 0, 0))
            tela.blit(texto_porta, (porta_rect_tela.x + 5, porta_rect_tela.y + 35))

            if porta_ativa and player.colliderect(porta):
                fase5()  # Chama a próxima fase (fase 5)

        # Exibe a pontuação
        texto_pontos = pixel_font.render(f"Pontos: {pontos}", True, (255, 255, 255))
        tela.blit(texto_pontos, (1080, 20))

        pygame.display.flip()  # Atualiza a tela
        clock.tick(60)  # Controla a taxa de quadros por segundo (FPS)
