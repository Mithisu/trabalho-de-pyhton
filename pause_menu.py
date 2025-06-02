import pygame
import sys

NOMES_DAS_FASES = {
    1: "Fase 1: Operações",
    2: "Fase 2: Inteiros",
    3: "Fase 3: Porcentagem",
    4: "Fase 4: Equação 1º",
    5: "Fase 5: Desafio Final"
}

def pause_menu(screen, Daydream, fase_numero):
    nome_fase = NOMES_DAS_FASES.get(fase_numero, f"Fase {fase_numero}")

    # Fontes
    fase_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 26)
    titulo_font = pygame.font.Font("assets/fonts/Daydream.ttf", 72)  # Título "PAUSE"
    botao_font = pygame.font.Font("assets/fonts/Daydream.ttf", 32)   # Botões

    width, height = screen.get_size()

    button_width = 400
    button_height = 60

    resume_button_rect = pygame.Rect(
        (width // 2 - button_width // 2, height // 2 + 50),
        (button_width, button_height)
    )

    menu_button_rect = pygame.Rect(
        (width // 2 - button_width // 2, height // 2 + 130),
        (button_width, button_height)
    )

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "resume"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_button_rect.collidepoint(event.pos):
                    return "resume"
                elif menu_button_rect.collidepoint(event.pos):
                    return "menu"

        mouse_pos = pygame.mouse.get_pos()

        screen.fill((0, 0, 0))  # Fundo preto

        # Título "PAUSE"
        titulo_text = titulo_font.render("PAUSE", True, (255, 255, 255))
        titulo_rect = titulo_text.get_rect(center=(width // 2, 200))
        screen.blit(titulo_text, titulo_rect)

        # Nome da fase (ajuste a posição se quiser mais pra baixo)
        fase_text = fase_font.render(nome_fase, True, (200, 200, 200))
        fase_rect = fase_text.get_rect(center=(width // 2, 280))
        screen.blit(fase_text, fase_rect)

        # Hover resume
        resume_hover = resume_button_rect.collidepoint(mouse_pos)
        resume_color = (204, 24, 24) if resume_hover else (255, 255, 255)
        resume_text = botao_font.render("Resume", True, resume_color)
        resume_text_rect = resume_text.get_rect(center=resume_button_rect.center)
        screen.blit(resume_text, resume_text_rect)

        # Hover menu
        menu_hover = menu_button_rect.collidepoint(mouse_pos)
        menu_color = (204, 24, 24) if menu_hover else (255, 255, 255)
        menu_text = botao_font.render("Menu", True, menu_color)
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        screen.blit(menu_text, menu_text_rect)

        pygame.display.flip()
        clock.tick(60)
