# Importa os módulos necessários
import pygame
import sys

# Dicionário que relaciona o número da fase com seu nome descritivo
NOMES_DAS_FASES = {
    1: "Fase 1: Operações",
    2: "Fase 2: Inteiros",
    3: "Fase 3: Porcentagem",
    4: "Fase 4: Equação 1º",
    5: "Fase 5: Desafio Final"
}

# Função que exibe o menu de pausa
def pause_menu(screen, Daydream, fase_numero):
    # Recupera o nome da fase atual com base no número recebido
    nome_fase = NOMES_DAS_FASES.get(fase_numero, f"Fase {fase_numero}")

    # Carrega a fonte da fase com tamanho 26
    fase_font = pygame.font.Font("assets/fonts/Daydream.ttf", 26)

    # Pega o tamanho da tela (largura e altura)
    width, height = screen.get_size()

    # Define a área retangular central onde os botões serão desenhados
    overlay_rect = pygame.Rect(width // 2 - 300, height // 2 - 200, 600, 400)

    # Carrega e ajusta a imagem de fundo para o tamanho da tela
    background_image = pygame.image.load("assets/imagens/pause.png").convert()
    background_image = pygame.transform.scale(background_image, (width, height))

    # Define tamanho dos botões
    button_width = 500
    button_height = 70

    # Cria o botão de "Retomar" centralizado dentro da caixa
    resume_button_rect = pygame.Rect(
        (overlay_rect.centerx - button_width // 2, overlay_rect.top + 150),
        (button_width, button_height)
    )

    # Cria o botão de "Menu Principal"
    menu_button_rect = pygame.Rect(
        (overlay_rect.centerx - button_width // 2, overlay_rect.top + 240),
        (button_width, button_height)
    )

    clock = pygame.time.Clock()

    # Loop principal do menu de pausa
    while True:
        # Processa eventos do Pygame (como fechar janela, teclado e mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Tecla ESC retoma o jogo
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "resume"

            # Clique do mouse
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_button_rect.collidepoint(event.pos):
                    return "resume"  # Retoma o jogo
                elif menu_button_rect.collidepoint(event.pos):
                    return "menu"    # Volta ao menu principal

        # Desenha a imagem de fundo
        screen.blit(background_image, (0, 0))

        # Mostra o nome da fase atual
        fase_text = fase_font.render(nome_fase, True, (255, 255, 255))
        fase_rect = fase_text.get_rect(center=(overlay_rect.centerx, overlay_rect.top + 90))
        screen.blit(fase_text, fase_rect)

        # Desenha botão de "Retomar"
        pygame.draw.rect(screen, (0, 0, 0), resume_button_rect)  # Cor de fundo preta
        pygame.draw.rect(screen, (0, 200, 255), resume_button_rect, 3)  # Borda azul
        resume_text = fase_font.render("Rsesume", True, (255, 255, 255))  # ATENÇÃO: "Rsesume" tem um erro de digitação
        resume_text_rect = resume_text.get_rect(center=resume_button_rect.center)
        screen.blit(resume_text, resume_text_rect)

        # Desenha botão de "Menu Principal"
        pygame.draw.rect(screen, (0, 0, 0), menu_button_rect)
        pygame.draw.rect(screen, (0, 200, 255), menu_button_rect, 3)
        menu_text = fase_font.render("Menu", True, (255, 255, 255))
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        screen.blit(menu_text, menu_text_rect)

        # Atualiza a tela e limita o FPS para 60
        pygame.display.flip()
        clock.tick(60)
