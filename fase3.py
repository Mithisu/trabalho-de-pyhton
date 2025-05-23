import pygame  # Importa a biblioteca pygame para criar o jogo
import random  # Importa a biblioteca random para gerar números aleatórios
import sys  # Importa a biblioteca sys para lidar com o sistema operacional
from jogador import criar_jogador, mover_jogador, checar_interacoes  # Funções personalizadas para o jogador
from fase4 import fase4 
from pause_menu import pause_menu  # Função personalizada para o menu de pausa

# Função que gera uma equação de porcentagem simples, como "x% de y"
def gerar_equacao_porcentagem():
    porcentagem = random.randint(1, 50)  # Gera um número de 1 a 50 para porcentagem
    valor = random.randint(10, 200)      # Gera um valor entre 10 e 200
    resultado = (porcentagem / 100) * valor  # Calcula a porcentagem do valor
    pergunta = f"{porcentagem}% de {valor}"  # Formata a pergunta
    resposta = round(resultado, 2)  # Arredonda a resposta para 2 casas decimais
    return {"pergunta": pergunta, "resposta": resposta}  # Retorna o dicionário com a pergunta e a resposta

# Função que gera uma equação de regra de 3 simples, como "a está para b, como c está para ?"
def gerar_equacao_regra_de_3():
    a = random.randint(1, 50)  # Gera um número entre 1 e 50 para 'a'
    b = random.randint(1, 50)  # Gera um número entre 1 e 50 para 'b'
    c = random.randint(1, 50)  # Gera um número entre 1 e 50 para 'c'
    resultado = (b * c) / a  # Calcula o resultado da regra de 3
    pergunta = f"{a} está para {b} como {c} está para x"  # Formata a pergunta
    resposta = round(resultado, 2)  # Arredonda a resposta para 2 casas decimais
    return {"pergunta": pergunta, "resposta": resposta}  # Retorna o dicionário com a pergunta e a resposta

# Função para a fase 3 do jogo
def fase3():
    pygame.init()  # Inicializa o Pygame
    tela = pygame.display.set_mode((1280, 720))  # Define o tamanho da tela
    pygame.display.set_caption("Missão: Código Secreto - Fase 3")  # Define o título da janela

    try:
        pixel_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 32)  # Tenta carregar uma fonte personalizada
    except:
        pixel_font = pygame.font.SysFont("Courier", 32)  # Caso falhe, usa a fonte padrão

    WORLD_WIDTH = 2560  # Largura do mundo (tela maior do que a visível)
    WORLD_HEIGHT = 1440  # Altura do mundo

    # Cria o jogador com as dimensões do mundo
    player, player_speed = criar_jogador(WORLD_WIDTH, WORLD_HEIGHT)
    jogador_carregando = None  # Inicializa a variável para armazenar o item que o jogador está carregando

    # Gera duas equações (porcentagem e regra de 3)
    equacoes = [gerar_equacao_porcentagem(), gerar_equacao_regra_de_3()]

    # Define as posições aleatórias para as equações na tela
    for eq in equacoes:
        eq["rect"] = pygame.Rect(
            random.randint(100, WORLD_WIDTH - 100),
            random.randint(100, WORLD_HEIGHT - 100),
            300, 60
        )
        eq["resolvida"] = False  # Marca as equações como não resolvidas inicialmente

    respostas = []
    # Gera respostas corretas para as equações
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
    # Gera alternativas erradas (números aleatórios) que não são respostas corretas
    while len(alternativas_erradas) < 4:
        alt_errada = round(random.uniform(1, 200), 2)  # Gera alternativas erradas
        if alt_errada not in [r["valor"] for r in respostas]:  # Verifica se a alternativa errada já existe nas respostas
            alternativas_erradas.add(alt_errada)

    # Adiciona as alternativas erradas à lista de respostas
    for alt in alternativas_erradas:
        respostas.append({
            "valor": alt,
            "rect": pygame.Rect(
                random.randint(100, WORLD_WIDTH - 100),
                random.randint(100, WORLD_HEIGHT - 100),
                50, 50
            )
        })

    porta = pygame.Rect(2400, 1200, 100, 100)  # Define a posição e tamanho da porta para avançar para a próxima fase
    porta_ativa = False  # Define a porta como desativada inicialmente

    pontos = 0  # Inicializa os pontos do jogador
    clock = pygame.time.Clock()  # Cria o objeto clock para controlar a taxa de atualização
    running = True  # Variável que controla o loop do jogo

    while running:
        tela.fill((30, 30, 30))  # Preenche a tela com a cor cinza escuro

        # Processa os eventos (como pressionamento de teclas ou fechamento da janela)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Fecha o Pygame
                sys.exit()  # Encerra o programa
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                fase_atual = 3
                acao_pause = pause_menu(tela, pixel_font, fase_atual)  # Abre o menu de pausa
                if acao_pause == "menu":
                    return "menu"  # Volta ao menu principal

        keys = pygame.key.get_pressed()  # Captura as teclas pressionadas
        player = mover_jogador(player, player_speed, keys, WORLD_WIDTH, WORLD_HEIGHT)  # Move o jogador
        coletar, dropar = checar_interacoes(keys)  # Verifica se o jogador pode coletar ou dropar um item

        # Define o deslocamento da câmera com base na posição do jogador
        offset_x = player.x - 1280 // 2 + player.width // 2
        offset_y = player.y - 720 // 2 + player.height // 2

        if jogador_carregando is None:
            # Verifica se o jogador está perto de uma resposta e a coleta
            for resposta in respostas:
                if player.colliderect(resposta["rect"]) and coletar:
                    jogador_carregando = resposta  # O jogador começa a carregar a resposta
                    respostas.remove(resposta)  # Remove a resposta da lista
                    break

        if jogador_carregando and dropar:
            # Se o jogador pressionar para dropar o item, ele será colocado no chão
            jogador_carregando["rect"].x = player.x + player.width // 2 - jogador_carregando["rect"].width // 2
            jogador_carregando["rect"].y = player.y + player.height // 2 - jogador_carregando["rect"].height // 2
            respostas.append(jogador_carregando)  # Adiciona o item de volta às respostas
            jogador_carregando = None  # Remove o item que o jogador estava carregando

        if jogador_carregando:
            # Verifica se o jogador acertou a equação com a resposta certa
            for eq in equacoes:
                if player.colliderect(eq["rect"]) and not eq["resolvida"]:
                    if round(jogador_carregando["valor"], 2) == round(eq["resposta"], 2):  # Verifica se a resposta está correta
                        pontos += 1  # Incrementa os pontos
                        eq["resolvida"] = True  # Marca a equação como resolvida
                        jogador_carregando = None  # Remove o item carregado
                    else:
                        jogador_carregando = None  # Se a resposta estiver errada, o jogador solta o item
                    break

        # Desenha as equações na tela
        for eq in equacoes:
            cor = (0, 255, 0) if eq["resolvida"] else (255, 100, 100)  # Verde para resolvidas, vermelho para não resolvidas
            rect = eq["rect"].copy()
            rect.x -= offset_x  # Ajusta a posição do retângulo da equação com base no deslocamento da câmera
            rect.y -= offset_y
            pygame.draw.rect(tela, cor, rect)  # Desenha o retângulo
            texto = pixel_font.render(eq["pergunta"], True, (0, 0, 0))  # Renderiza a pergunta da equação
            tela.blit(texto, (rect.x + 10, rect.y + 15))  # Exibe a pergunta

        # Desenha as respostas na tela
        for resposta in respostas:
            rect = resposta["rect"].copy()
            rect.x -= offset_x
            rect.y -= offset_y
            pygame.draw.rect(tela, (255, 255, 0), rect)  # Desenha a resposta em amarelo
            texto = pixel_font.render(str(resposta["valor"]), True, (0, 0, 0))  # Renderiza a resposta
            tela.blit(texto, (rect.x + 5, rect.y + 5))  # Exibe a resposta

        # Desenha o jogador na tela
        player_rect_tela = pygame.Rect(
            1280 // 2 - player.width // 2,
            720 // 2 - player.height // 2,
            player.width,
            player.height
        )
        pygame.draw.rect(tela, (0, 200, 255), player_rect_tela)  # Desenha o jogador

        if jogador_carregando:
            texto_item = pixel_font.render(
                f"Carregando: {round(jogador_carregando['valor'], 2)}",
                True,
                (255, 255, 255)
            )
            tela.blit(texto_item, (20, 660))  # Exibe o valor do item que o jogador está carregando

        if pontos == len(equacoes):
            porta_ativa = True  # Ativa a porta se o jogador tiver resolvido todas as equações

        if porta_ativa:
            porta_rect_tela = porta.copy()
            porta_rect_tela.x -= offset_x
            porta_rect_tela.y -= offset_y
            pygame.draw.rect(tela, (0, 0, 255), porta_rect_tela)  # Desenha a porta
            texto_porta = pixel_font.render("Ir para próxima fase", True, (0, 0, 0))  # Exibe o texto na porta
            tela.blit(texto_porta, (porta_rect_tela.x + 10, porta_rect_tela.y + 35))

        if porta_ativa and player.colliderect(porta):
            fase4()  # Avança para a próxima fase se o jogador colidir com a porta

        texto_pontos = pixel_font.render(f"Pontos: {pontos}", True, (255, 255, 255))
        tela.blit(texto_pontos, (1080, 20))  # Exibe os pontos do jogador

        pygame.display.flip()  # Atualiza a tela
        clock.tick(60)  # Define o FPS para 60
