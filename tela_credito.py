import pygame

def tela_creditos(screen):
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))

        # Fontes
        titulo_font = pygame.font.Font("assets/fonts/Daydream.ttf", 60)
        texto_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 25)

        # Títulos e nomes
        texto_titulo = titulo_font.render("CREDITS", True, (255, 255, 255))
        texto_creditos = texto_font.render("Desenvolvido por:", True, (255, 255, 255))
        nome1 = texto_font.render("Danillo Augusto ", True, (255, 255, 255))
        nome2 = texto_font.render("Henrique", True, (255, 255, 255))
        nome3 = texto_font.render("Weberson", True, (255, 255, 255))
        nome4 = texto_font.render("Higor", True, (255, 255, 255))
        nome5 = texto_font.render("Renato", True, (255, 255, 255))
        info = texto_font.render("Presione ESC para sair", True, (204, 24, 24))

        # Posicionamento centralizado
        center_x = screen.get_width() // 2
        y_base = 300
        espacamento = 40

        screen.blit(texto_titulo, (center_x - texto_titulo.get_width() // 2, 60))
        screen.blit(texto_creditos, (center_x - texto_creditos.get_width() // 2, 150))
        screen.blit(nome1, (center_x - nome1.get_width() // 2, y_base + espacamento * 1))
        screen.blit(nome2, (center_x - nome2.get_width() // 2, y_base + espacamento * 2))
        screen.blit(nome3, (center_x - nome3.get_width() // 2, y_base + espacamento * 3))
        screen.blit(nome4, (center_x - nome4.get_width() // 2, y_base + espacamento * 4))
        screen.blit(nome5, (center_x - nome5.get_width() // 2, y_base + espacamento * 5))
        screen.blit(info, (center_x - info.get_width() // 2, y_base + espacamento * 7))

        pygame.display.flip()
        clock.tick(60)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
