# Importa os módulos necessários
import pygame
import pygame_gui
import sys

# Inicializa todos os módulos do Pygame
pygame.init()

# Define as dimensões da janela do jogo
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Cria a janela
pygame.display.set_caption("Missão Código Secreto")  # Define o título da janela

# Cria o gerenciador da interface gráfica (pygame_gui)
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Define cores usadas no texto (branco e destaque)
WHITE = (255, 255, 255)
HIGHLIGHT = (204, 24, 24)

# Tenta carregar uma fonte personalizada no estilo pixel art.
# Se não encontrar, usa uma fonte padrão do sistema.
try:
    pixel_font = pygame.font.Font("assets/fonts/Daydream.ttf", 48)
except:
    pixel_font = pygame.font.SysFont("Courier", 48)

# Carrega a imagem de fundo e ajusta ao tamanho da janela
background = pygame.image.load("assets/imagens/menu_jogo.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Configura os "botões invisíveis" (retângulos que detectam cliques)
button_height = 70
left_margin = 60  # Margem esquerda onde os botões começam

# Cria um dicionário com os botões e suas posições
buttons = {
    "Start": pygame.Rect(left_margin, 360, 250, button_height),
    "Credits": pygame.Rect(left_margin, 470, 350, button_height),
    "Exit": pygame.Rect(left_margin, 580, 200, button_height)
}

# Função que desenha o menu na tela
def draw_menu():
    screen.blit(background, (0, 0))  # Desenha o fundo

    # Para cada botão, renderiza o texto e aplica o destaque se o mouse estiver em cima
    for text, rect in buttons.items():
        mouse_over = rect.collidepoint(pygame.mouse.get_pos())  # Verifica se o mouse está sobre o botão
        color = HIGHLIGHT if mouse_over else WHITE  # Muda a cor do texto se o botão estiver em foco

        label = pixel_font.render(text, True, color)  # Renderiza o texto do botão

        # Desenha o texto alinhado à esquerda dentro do botão
        screen.blit(label, (
            rect.x,
            rect.y + (rect.height - label.get_height()) // 2  # Centraliza verticalmente
        ))

    pygame.display.flip()  # Atualiza a tela com o novo conteúdo

# Função principal do menu
def main_menu():
    clock = pygame.time.Clock()  # Relógio para controlar FPS
    while True:
        time_delta = clock.tick(60) / 1000.0  # Tempo entre frames

        # Trata os eventos (cliques, fechamento da janela, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for text, rect in buttons.items():
                    if rect.collidepoint(event.pos):  # Verifica se clicou em um botão
                        if text == "Start":
                            import fase5 # Importa o módulo da fase (deve existir)
                            fase5.fase5()  # Chama a função da fase
                        elif text == "Credits":
                            import tela_credito
                            tela_credito.tela_creditos(screen)  # Mostra os créditos no terminal
                        elif text == "Exit":
                            pygame.quit()
                            sys.exit()

            manager.process_events(event)  # Processa eventos do pygame_gui (não utilizados aqui, mas prontos para expansão)

        manager.update(time_delta)  # Atualiza o estado da interface
        draw_menu()  # Redesenha o menu a cada frame

# Executa o menu se o arquivo for rodado diretamente
if __name__ == "__main__":
    main_menu()
