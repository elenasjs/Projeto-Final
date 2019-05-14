import pygame
import pygame.locals
from random import randrange
import sys, pygame

jogando = 1
pygame.init()
definicao = width, height = 1000, 800
tela = pygame.display.set_mode(definicao)

class Jogador(pygame.sprite.Sprite):

    def __init__(self,foto_peao,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(foto_peao)
        self.image = pygame.transform.scale(self.image,(170,100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Fundo(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tabuleiro.jpg").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


while jogando:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit() 
	pygame.display.update()
	pygame.display.flip()