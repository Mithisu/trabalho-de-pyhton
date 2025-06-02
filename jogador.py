import pygame
import os

class Jogador(pygame.sprite.Sprite):
    def __init__(self, world_width, world_height):
        super().__init__()
        self.animacoes = {
            "idle": self.carregar_animacoes("assets/personagem/idle"),
            "andar": self.carregar_animacoes("assets/personagem/walk"),
            "correr": self.carregar_animacoes("assets/personagem/run"),
            "coletar": self.carregar_animacoes("assets/personagem/pick_iten"),
            "dropar": self.carregar_animacoes("assets/personagem/pick_iten")
        }

        self.virado_para_direita = True
        
        self.estado = "idle"
        self.frame = 0
        self.image = self.animacoes[self.estado][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (world_width // 2, world_height // 2)

        # Colisão menor
        self.hitbox = pygame.Rect(0, 0, 50, 50)
        self.hitbox.center = self.rect.center

        self.velocidade_base = 5
        self.velocidade_corrida = self.velocidade_base * 2
        self.direcao = pygame.math.Vector2(0, 0)

        self.contador_animacao = 0
        self.frequencia_animacao = 5

        self.acao_em_execucao = None
        self.contador_acao = 0
        self.frame_max_acao = len(self.animacoes["coletar"])

    def carregar_animacoes(self, pasta):
        animacoes = []
        for nome_arquivo in sorted(os.listdir(pasta)):
            caminho = os.path.join(pasta, nome_arquivo)
            imagem = pygame.image.load(caminho).convert_alpha()
            imagem = pygame.transform.scale(imagem, (160, 160))  # Ajuste o tamanho aqui
            animacoes.append(imagem)
        return animacoes
    

    def atualizar_estado(self, keys):
        if self.acao_em_execucao:
            return

        self.direcao.x = 0
        self.direcao.y = 0
        velocidade = self.velocidade_corrida if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else self.velocidade_base

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direcao.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direcao.y = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direcao.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direcao.x = 1

        if self.direcao.length() != 0:
            self.direcao = self.direcao.normalize()
            self.estado = "correr" if velocidade > self.velocidade_base else "andar"
            self.hitbox.x += self.direcao.x * velocidade
            self.hitbox.y += self.direcao.y * velocidade
            self.rect.center = self.hitbox.center 
        else:
            self.estado = "idle"

        if self.direcao.x < 0:
            self.virado_para_direita = False
        elif self.direcao.x > 0:
            self.virado_para_direita = True

    def limitar_area(self, world_width, world_height):
       self.hitbox.x = max(0, min(self.hitbox.x, world_width - self.hitbox.width))
       self.hitbox.y = max(0, min(self.hitbox.y, world_height - self.hitbox.height))
       self.rect.center = self.hitbox.center

    def atualizar_animacao(self):
        self.contador_animacao += 1
        if self.contador_animacao >= self.frequencia_animacao:
            self.contador_animacao = 0
            self.frame += 1

            centro_anterior = self.rect.center

            if self.acao_em_execucao:
                if self.frame >= len(self.animacoes[self.acao_em_execucao]):
                    self.acao_em_execucao = None
                    self.frame = 0
                    self.estado = "idle"
                    imagem_original = self.animacoes[self.estado][self.frame]
                    self.image = pygame.transform.flip(imagem_original, not self.virado_para_direita, False) 
                else:
                    self.image = self.animacoes[self.acao_em_execucao][self.frame]
            else:
                self.frame = self.frame % len(self.animacoes[self.estado])
                imagem_original = self.animacoes[self.estado][self.frame]
                self.image = pygame.transform.flip(imagem_original, not self.virado_para_direita, False)

            self.rect = self.image.get_rect()
            self.rect.center = self.hitbox.center

    def executar_acao(self, acao):
        if not self.acao_em_execucao:
            self.acao_em_execucao = acao
            self.frame = 0
            centro_anterior = self.rect.center
            self.image = self.animacoes[acao][self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = self.hitbox.center

    def update(self, keys, world_width, world_height):
        self.atualizar_estado(keys)
        self.limitar_area(world_width, world_height)
        self.atualizar_animacao()

    def checar_interacoes(self, keys):
        if keys[pygame.K_e]:
            self.executar_acao("coletar")
            return True, False
        elif keys[pygame.K_q]:
            self.executar_acao("dropar")
            return False, True
        return False, False
