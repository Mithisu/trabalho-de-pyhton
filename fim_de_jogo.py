# Importa as bibliotecas necessárias
import pygame
import sys
import pygame_gui  # Biblioteca para facilitar criação de interfaces com botões e menus

# Função que exibe a tela final do jogo
def tela_final(screen, pixel_font, button_width=600, button_height=70):
    # Pega o tamanho da tela
    width, height = screen.get_size()

    # Inicializa o relógio do pygame para controle do tempo (FPS)
    clock = pygame.time.Clock()

    # Cria o gerenciador de interface (UI Manager) do pygame_gui com o tamanho da tela
    manager = pygame_gui.UIManager((width, height))

    # Cria um botão centralizado na tela, com o texto "Voltar ao Menu"
    button_voltar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (width // 2 - button_width // 2, height // 2 + 150),  # Posição do botão
            (button_width, button_height)  # Tamanho do botão
        ),
        text='Voltar ao Menu',
        manager=manager  # Interface responsável por gerenciar o botão
    )

    # Loop principal da tela final (fica ativo até o jogador sair ou clicar no botão)
    while True:
        # Calcula o tempo entre os frames (em segundos)
        time_delta = clock.tick(60) / 1000.0

        # Verifica os eventos (teclado, mouse, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Se pressionar ESC, volta ao menu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

            # Entrega o evento para o gerenciador da interface
            manager.process_events(event)

            # Verifica se algum botão foi clicado
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # Se o botão clicado for o "Voltar ao Menu", retorna para o menu
                if event.ui_element == button_voltar:
                    return "menu"

        # Atualiza o gerenciador de interface com o tempo decorrido
        manager.update(time_delta)

        # Preenche o fundo da tela com cinza escuro
        screen.fill((15, 15, 15))

        # Renderiza o título "THE END" em azul neon e o posiciona no topo da tela
        titulo_surf = pixel_font.render("THE END", True, (0, 255, 255))
        titulo_rect = titulo_surf.get_rect(center=(width // 2, height // 2 - 130))
        screen.blit(titulo_surf, titulo_rect)

        # Lista de linhas com os créditos finais
        creditos = [
            "Desenvolvido por:",
            "Seu Nome Aqui",
            "",
            "Projeto: Missão Código Secreto",
            "",
            "Obrigado por jogar!"
        ]

        # Renderiza e posiciona cada linha de crédito na tela
        for i, linha in enumerate(creditos):
            cor = (180, 180, 180)  # Cor cinza clara
            texto_surf = pixel_font.render(linha, True, cor)
            texto_rect = texto_surf.get_rect(center=(width // 2, height // 2 - 40 + i * 30))
            screen.blit(texto_surf, texto_rect)

        # Desenha os elementos da interface (como o botão) na tela
        manager.draw_ui(screen)

        # Atualiza a tela com todas as mudanças
        pygame.display.flip()

        # Controla a taxa de atualização (60 quadros por segundo)
        clock.tick(60)
