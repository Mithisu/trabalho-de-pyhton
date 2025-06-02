# Importa a biblioteca pygame
import pygame

# Função que exibe a tela de "Game Over"
def game_over(screen, font):
    # Loop principal da tela de Game Over (fica ativo até o jogador tomar uma decisão)
      while True:
        screen.fill((0, 0, 0))

        texto_game_over = font.render("Game Over", True, (255, 0, 0))
        texto_linha1 = font.render("Pressione R para reiniciar", True, (255, 255, 255))
        texto_linha2 = font.render("ou ESC para sair", True, (255, 255, 255))

        screen.blit(
            texto_game_over,
            (screen.get_width() // 2 - texto_game_over.get_width() // 2, 200)
        )
        screen.blit(
            texto_linha1,
            (screen.get_width() // 2 - texto_linha1.get_width() // 2, 440)
        )
        screen.blit(
            texto_linha2,
            (screen.get_width() // 2 - texto_linha2.get_width() // 2, 480)
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
                    return "reiniciar"
                # Pressionar "ESC" sai do jogo
                if event.key == pygame.K_ESCAPE:
                    return "sair"
