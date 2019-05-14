import pygame
import pygame.locals
from random import randrange
import sys, pygame

jogando = true

pygame.init()
definicao = width, height = 1000, 800
tabuleiro = pygame.image.load("tabuleiro.png")
tela = pygame.display.set_mode(size)

while jogando:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit() 
	tela.blit(tabuleiro, (0,0))
	pygame.display.flip()