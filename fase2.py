import pygame  # Importa a biblioteca pygame para criar o jogo
import sys  # Importa o módulo sys, usado para controlar a execução do jogo, como fechar o programa
import random  # Importa a biblioteca random para gerar números aleatórios
from jogador import criar_jogador, mover_jogador, checar_interacoes  # Funções para criar e mover o jogador, e verificar interações
from fase3 import fase3  # Importa a função da próxima fase
from pause_menu import pause_menu  # Importa a função do menu de pausa
from game_over import game_over 
from status_jogador import StatusJogador  # Importa a classe de status

# Função que gera uma equação de soma ou subtração com números inteiros aleatórios
def gerar_equacao_inteiros():
    op = random.choice(["+", "-"])  # Escolhe aleatoriamente entre soma e subtração
    if op == "+":
        num1 = random.randint(-50, 50)  # Gera um número aleatório entre -50 e 50
        num2 = random.randint(-50, 50)  # Gera outro número aleatório entre -50 e 50
        resposta = num1 + num2  # Realiza a soma
    else:
        num1 = random.randint(-50, 50)  # Gera um número aleatório entre -50 e 50
        num2 = random.randint(-50, 50)  # Gera outro número aleatório entre -50 e 50
        resposta = num1 - num2  # Realiza a subtração

    pergunta = f"{num1} {op} {num2}"  # Formata a equação em string
    return {"pergunta": pergunta, "resposta": resposta}  # Retorna um dicionário com a pergunta e a resposta

# Função que define o comportamento da Fase 2 do jogo
def fase2():
    pygame.init()  # Inicializa a biblioteca pygame
    tela = pygame.display.set_mode((1280, 720))  # Cria a janela do jogo com resolução 1280x720
    pygame.display.set_caption("Missão: Código Secreto - Fase 2")  # Define o título da janela

    try:
        pixel_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 32)  # Tenta carregar uma fonte personalizada
    except:
        pixel_font = pygame.font.SysFont("Courier", 32)  # Se não conseguir, usa a fonte Courier do sistema

    WORLD_WIDTH = 2560  # Define a largura do mundo do jogo
    WORLD_HEIGHT = 1440  # Define a altura do mundo do jogo

    player, player_speed = criar_jogador(WORLD_WIDTH, WORLD_HEIGHT)  # Cria o jogador e define sua velocidade
    jogador_carregando = None  # Variável que vai armazenar o item que o jogador está carregando

    # Inicializa o status do jogador (vidas e pontos)
    status = StatusJogador()

    # Cria 3 equações e armazena elas em uma lista
    equacoes = [gerar_equacao_inteiros() for _ in range(3)]  
    # Para cada equação, define uma posição aleatória na tela e se a equação já foi resolvida
    for eq in equacoes:
        eq["rect"] = pygame.Rect(random.randint(100, WORLD_WIDTH - 100),
                                 random.randint(100, WORLD_HEIGHT - 100), 160, 60)  # Define a posição da equação
        eq["resolvida"] = False  # Inicialmente, a equação não foi resolvida

    # Cria as respostas (correspondentes às equações)
    respostas = [
        {"valor": eq["resposta"],
         "rect": pygame.Rect(random.randint(100, WORLD_WIDTH - 100),
                             random.randint(100, WORLD_HEIGHT - 100), 50, 50)}
        for eq in equacoes
    ]

    # Adiciona algumas respostas incorretas para confundir o jogador
    for _ in range(3):
        valor_errado = random.randint(-100, 100)
        while valor_errado in [r["valor"] for r in respostas]:  # Garante que a resposta errada seja única
            valor_errado = random.randint(-100, 100)
        respostas.append({
            "valor": valor_errado,  # Adiciona uma resposta errada
            "rect": pygame.Rect(random.randint(100, WORLD_WIDTH - 100),
                                random.randint(100, WORLD_HEIGHT - 100), 50, 50)
        })

    porta = pygame.Rect(2400, 1200, 100, 100)  # Cria a "porta" de saída para a próxima fase
    porta_ativa = False  # Inicialmente, a porta não está ativa

    clock = pygame.time.Clock()  # Controla a taxa de atualização do jogo (FPS)
    running = True  # Variável que controla o loop principal do jogo

    # Loop principal do jogo
    while running:
        tela.fill((30, 30, 30))  # Preenche a tela com a cor de fundo (cinza escuro)

        # Verifica os eventos que ocorrem no jogo (como pressionamento de teclas ou fechamento da janela)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Encerra o jogo
                sys.exit()  # Fecha a aplicação
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Abre o menu de pausa ao pressionar a tecla ESC
                acao_pause = pause_menu(tela, pixel_font)  # Chama o menu de pausa
                if acao_pause == "menu":
                    return "menu"  # Se o jogador escolheu sair para o menu principal
                # Se for "resume", continua o jogo normalmente

        # Obtém o estado das teclas pressionadas
        keys = pygame.key.get_pressed()
        player = mover_jogador(player, player_speed, keys, WORLD_WIDTH, WORLD_HEIGHT)  # Atualiza a posição do jogador
        coletar, dropar = checar_interacoes(keys)  # Checa se o jogador está coletando ou soltando itens

        # Calcula o deslocamento da câmera para centralizar o jogador na tela
        offset_x = player.x - 1280 // 2 + player.width // 2
        offset_y = player.y - 720 // 2 + player.height // 2

        # Verifica se o jogador está perto de alguma resposta para coletá-la
        if jogador_carregando is None:
            for resposta in respostas:
                if player.colliderect(resposta["rect"]) and coletar:
                    jogador_carregando = resposta  # O jogador começa a carregar a resposta
                    respostas.remove(resposta)  # Remove a resposta da tela
                    break

        # Verifica se o jogador está carregando um item e se ele soltar o item
        if jogador_carregando and dropar:
            jogador_carregando["rect"].x = player.x + player.width // 2 - jogador_carregando["rect"].width // 2
            jogador_carregando["rect"].y = player.y + player.height // 2 - jogador_carregando["rect"].height // 2
            respostas.append(jogador_carregando)  # Adiciona a resposta de volta na tela
            jogador_carregando = None  # Reseta a variável de jogador carregando

        # Verifica se o jogador está perto de uma equação e se ele tem a resposta correta
        if jogador_carregando:
            for eq in equacoes:
                if player.colliderect(eq["rect"]) and not eq["resolvida"]:
                    if jogador_carregando["valor"] == eq["resposta"]:
                        status.ganhar_pontos(100)  # Chama a função para ganhar pontos
                        eq["resolvida"] = True  # Marca a equação como resolvida
                        status.ganhar_pontos(250)
                        jogador_carregando = None  # Reseta o item carregado
                    else:
                        status.perder_vida()  # <-- Novo: perde vida ao errar
                        if status.game_over():  # <-- Novo: verifica fim de jogo
                            acao = game_over(tela, pixel_font)
                            if acao == "reiniciar":
                                return fase2()
                            elif acao == "sair":
                                return "menu"

                    jogador_carregando = None

        # Desenha as equações na tela, com cores diferentes dependendo se foram resolvidas ou não
        for eq in equacoes:
            cor = (0, 255, 0) if eq["resolvida"] else (255, 100, 100)
            rect = eq["rect"].copy()
            rect.x -= offset_x
            rect.y -= offset_y
            pygame.draw.rect(tela, cor, rect)  # Desenha o retângulo da equação
            texto = pixel_font.render(eq["pergunta"], True, (0, 0, 0))
            tela.blit(texto, (rect.x + 10, rect.y + 15))  # Desenha o texto da equação

        # Desenha as respostas na tela
        for resposta in respostas:
            rect = resposta["rect"].copy()
            rect.x -= offset_x
            rect.y -= offset_y
            pygame.draw.rect(tela, (255, 255, 0), rect)  # Desenha o retângulo da resposta
            texto = pixel_font.render(str(resposta["valor"]), True, (0, 0, 0))
            tela.blit(texto, (rect.x + 5, rect.y + 5))  # Desenha o valor da resposta

        # Desenha o jogador na tela
        player_rect_tela = pygame.Rect(1280 // 2 - player.width // 2,
                                       720 // 2 - player.height // 2, player.width, player.height)
        pygame.draw.rect(tela, (0, 200, 255), player_rect_tela)  # Desenha o retângulo do jogador

        # Exibe o item carregado pelo jogador, se houver
        if jogador_carregando:
            texto_item = pixel_font.render(f"Carregando: {jogador_carregando['valor']}", True, (255, 255, 255))
            tela.blit(texto_item, (20, 660))

        # Se todas as equações foram resolvidas, ativa a porta de saída
        if all(eq["resolvida"] for eq in equacoes):
            porta_ativa = True

        # Desenha a porta de saída, se estiver ativa
        if porta_ativa:
            porta_rect_tela = porta.copy()
            porta_rect_tela.x -= offset_x
            porta_rect_tela.y -= offset_y
            pygame.draw.rect(tela, (0, 0, 255), porta_rect_tela)
            texto_porta = pixel_font.render("Ir para próxima fase", True, (0, 0, 0))
            tela.blit(texto_porta, (porta_rect_tela.x + 10, porta_rect_tela.y + 35))

        # Se o jogador colidir com a porta, avança para a próxima fase
        if porta_ativa and player.colliderect(porta):
            fase3()  # Chama a próxima fase (fase 3)

        # Exibe a pontuação do jogador
        status.renderizar(tela, pixel_font)

        # Atualiza a tela a cada frame
        pygame.display.flip()
        clock.tick(60)  # Limita o FPS a 60
