# Importa a biblioteca pygame
import pygame


# Função que exibe a tela de "Game Over"
def game_over(screen, font):
      
    # Carrega a imagem do personagem morto
    personagem_morto = pygame.image.load("assets/imagens/game_over.png").convert_alpha()
    # Redimensiona se necessário
    personagem_morto = pygame.transform.scale(personagem_morto, (360, 360))

    # Loop principal da tela de Game Over (fica ativo até o jogador tomar uma decisão)
    while True:

        screen.fill((0, 0, 0))

        titulo_font = pygame.font.Font("assets/fonts/Daydream.ttf", 72) 
        texto_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 25)

        texto_game_over = titulo_font.render("Game Over", True, (204, 24, 24))
        texto_linha1 = texto_font.render("Pressione R para reiniciar o progresso", True, (204, 24, 24))
        texto_linha2 = texto_font.render("ou ESC para sair", True, (204, 24, 24))

        screen.blit(
           personagem_morto,
           (screen.get_width() // 2 - personagem_morto.get_width() // 2, 170)
        )

        screen.blit(
            texto_game_over,
            (screen.get_width() // 2 - texto_game_over.get_width() // 2, 150)
        )
        screen.blit(
            texto_linha1,
            (screen.get_width() // 2 - texto_linha1.get_width() // 2, 580)
        )
        screen.blit(
            texto_linha2,
            (screen.get_width() // 2 - texto_linha2.get_width() // 2, 620)
        )

        pygame.display.flip()

        # Processa os eventos do pygame (teclado, fechar janela, etc.)
        for event in pygame.event.get():
            # Se o usuário fechar a janela, finaliza o pygame e encerra o programa
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Se o usuário pressionar uma tecla
            if event.type == pygame.KEYDOWN:
                # Pressionar "R" reinicia o jogo
                if event.key == pygame.K_r:
                    import fase1
                    fase1.fase1()
                # Pressionar "ESC" sai do jogo
                if event.key == pygame.K_ESCAPE:
                    return "sair"
