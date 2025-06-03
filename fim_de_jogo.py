import pygame

def tela_final(screen):
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))

        # Fontes
        titulo_font = pygame.font.Font("assets/fonts/Daydream.ttf", 72) 
        botao_font = pygame.font.Font("assets/fonts/Daydream.ttf", 45) 
        texto_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 25)

        # Renderização dos textos
        texto_end = titulo_font.render("The END", True, (204, 24, 24))
        texto_creditos = texto_font.render("FEITO POR:", True, (255, 255, 255))
        texto_danillo = texto_font.render("Danillo", True, (255, 255, 255))
        texto_henrique = texto_font.render("Henrique", True, (255, 255, 255))
        texto_weberson = texto_font.render("Weberson", True, (255, 255, 255))
        texto_higor = texto_font.render("Higor", True, (255, 255, 255))
        texto_obg = texto_font.render("Obrigado por jogar!", True, (255, 255, 255))

        # Título
        screen.blit(texto_end, (screen.get_width() // 2 - texto_end.get_width() // 2, 100))
        

        # Créditos com mais espaçamento e mais abaixo
        y_base = 270
        espacamento = 40
        screen.blit(texto_creditos, (screen.get_width() // 2 - texto_creditos.get_width() // 2, y_base))
        screen.blit(texto_danillo, (screen.get_width() // 2 - texto_danillo.get_width() // 2, y_base + espacamento))
        screen.blit(texto_henrique, (screen.get_width() // 2 - texto_henrique.get_width() // 2, y_base + espacamento * 2))
        screen.blit(texto_weberson, (screen.get_width() // 2 - texto_weberson.get_width() // 2, y_base + espacamento * 3))
        screen.blit(texto_higor, (screen.get_width() // 2 - texto_higor.get_width() // 2, y_base + espacamento * 4))

        # Obrigado (mais pra cima)
        screen.blit(texto_obg, (screen.get_width() // 2 - texto_obg.get_width() // 2, 540))

        # Botão MENU (hover apenas no texto)
        mouse_pos = pygame.mouse.get_pos()
        texto_menu = botao_font.render("MENU", True, (255, 255, 255))
        menu_rect = texto_menu.get_rect(center=(screen.get_width() // 2, 610))

        if menu_rect.collidepoint(mouse_pos):
            texto_menu = botao_font.render("MENU", True, (204, 24, 24))  # hover vermelho

        screen.blit(texto_menu, menu_rect)

        pygame.display.flip()
        clock.tick(60)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(mouse_pos):
                    return "menu"
