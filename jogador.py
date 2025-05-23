# Importa a biblioteca pygame
import pygame

# Função para criar o jogador
def criar_jogador(world_width, world_height):
    # Cria um retângulo (x, y, largura, altura) representando o jogador
    # A posição inicial é centralizada no mundo (world_width / 2, world_height / 2)
    jogador = pygame.Rect(world_width // 2, world_height // 2, 50, 50)

    # Define a velocidade base de movimento do jogador
    velocidade = 5
    return jogador, velocidade  # Retorna o retângulo do jogador e a velocidade

# Função para mover o jogador com base nas teclas pressionadas
def mover_jogador(jogador, velocidade, keys, world_width, world_height):
    # Define uma velocidade de corrida (duas vezes a velocidade base)
    velocidade_corrida = velocidade * 2

    # Se uma das teclas Shift estiver pressionada, usa a velocidade de corrida
    velocidade_atual = velocidade_corrida if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) else velocidade

    # Movimento para cima (W ou seta ↑)
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        jogador.y -= velocidade_atual
    # Movimento para baixo (S ou seta ↓)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        jogador.y += velocidade_atual
    # Movimento para a esquerda (A ou seta ←)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        jogador.x -= velocidade_atual
    # Movimento para a direita (D ou seta →)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        jogador.x += velocidade_atual

    # Impede o jogador de sair da área do mundo
    jogador.x = max(0, min(jogador.x, world_width - jogador.width))    # Limita no eixo X
    jogador.y = max(0, min(jogador.y, world_height - jogador.height))  # Limita no eixo Y

    return jogador  # Retorna o jogador atualizado

# Função para verificar se as teclas de interação foram pressionadas
def checar_interacoes(keys):
    coletar = keys[pygame.K_e]  # Tecla E para coletar itens
    dropar = keys[pygame.K_q]  # Tecla Q para dropar itens
    return coletar, dropar  # Retorna dois valores booleanos
