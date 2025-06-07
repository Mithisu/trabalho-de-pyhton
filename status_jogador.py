class StatusJogador:
    # Classe que gerencia o status do jogador, incluindo vidas e pontuação.

    def __init__(self, vidas_iniciais=3, vidas_max=5, score_por_vida=1000):
        # Inicializa o jogador com atributos:
        # - vidas_iniciais: Quantidade inicial de vidas (3 por padrão).
        # - vidas_max: Número máximo de vidas que pode ter (5 por padrão).
        # - score_por_vida: Pontuação necessária para ganhar uma vida extra (1000 pontos por padrão).
        
        self.vidas = vidas_iniciais  # Define as vidas iniciais do jogador.
        self.vidas_max = vidas_max  # Define o número máximo de vidas permitidas.
        self.pontos = 0  # Inicia o jogador com 0 pontos.
        self.score_por_vida = score_por_vida  # Define quantos pontos são necessários para ganhar uma vida extra.
        self._proxima_vida_em = score_por_vida  # Primeiro marco de pontuação necessário para ganhar uma vida.

    def perder_vida(self):
        # Método chamado quando o jogador erra.
        # Se ainda tiver vidas, ele perderá 1 vida.
        
        if self.vidas > 0:
            self.vidas -= 1  # Reduz uma vida do jogador.

    def ganhar_pontos(self, valor):
        # Adiciona pontos ao jogador e verifica se ele atingiu a pontuação necessária
        # para ganhar uma vida extra.
        # - valor: quantidade de pontos a ser adicionada.
        
        self.pontos += valor  # Adiciona os pontos obtidos ao total do jogador.

        # Verifica se atingiu o limite necessário para ganhar uma vida extra.
        if self.pontos >= self._proxima_vida_em and self.vidas < self.vidas_max:
            self.vidas += 1  # Adiciona uma vida ao jogador.
            self._proxima_vida_em += self.score_por_vida  # Atualiza o próximo limite de pontuação para ganhar vida.

    def game_over(self):
        # Verifica se o jogador perdeu todas as vidas.
        # Retorna True se o número de vidas for 0 ou menos.
        
        return self.vidas <= 0  # Retorna True caso o jogador tenha perdido todas as vidas.

    def renderizar(self, tela, fonte, pos_pontos=(20, 20), pos_vidas=(20, 60)):
        # Renderiza na tela as informações de pontuação e vidas do jogador.
        # - tela: Superfície onde os textos serão desenhados.
        # - fonte: Fonte usada para renderizar os textos.
        # - pos_pontos: Posição onde será desenhada a pontuação.
        # - pos_vidas: Posição onde serão desenhadas as vidas.

        texto_pontos = fonte.render(f"Pontos: {self.pontos}", True, (100, 100, 100))  # Texto branco para os pontos.
        texto_vidas = fonte.render(f"Vidas: {self.vidas}", True, (255, 0, 0))  # Texto vermelho para as vidas.
        tela.blit(texto_pontos, pos_pontos)  # Desenha o texto dos pontos na tela.
        tela.blit(texto_vidas, pos_vidas)  # Desenha o texto das vidas na tela.
