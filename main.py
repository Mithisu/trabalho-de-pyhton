# Importa o módulo pygame e as funções de cada fase e do menu principal
import pygame
from main_menu import main_menu
from fase1 import fase1
from fase2 import fase2
from fase3 import fase3
from fase4 import fase4
from fase5 import fase5

# Inicializa os módulos do Pygame
pygame.init()

# Cria a janela principal do jogo com resolução 1280x720
tela = pygame.display.set_mode((1280, 720))

# Define o título da janela
pygame.display.set_caption("Jogo de Matemática")

# Carrega a fonte no estilo pixel art com tamanho 50
pixel_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 50)

# Loop principal do jogo
while True:
    # Chama o menu principal e recebe a escolha do jogador (ex: "fase1", "sair", etc.)
    escolha = main_menu()

    # Com base na escolha, inicia a fase correspondente
    if escolha == "fase1":
        resultado = fase1(tela)
    elif escolha == "fase2":
        resultado = fase2(tela)
    elif escolha == "fase3":
        resultado = fase3(tela)
    elif escolha == "fase4":
        resultado = fase4(tela)
    elif escolha == "fase5":
        resultado = fase5(tela)
    else:
        break  # Encerra o jogo se a escolha for "sair" ou inválida

    # Se a fase retornar "menu", o jogo volta para o menu principal
    if resultado == "menu":
        continue  # Reinicia o loop, voltando ao menu
