from tkinter import *
import pygame
import pygame_menu
from pygame.locals import *
import sys
import random
window = Tk()



#Initializing pygame
pygame.init()
SCREEN_WIDTH = window.winfo_screenwidth()
SCREEN_HEIGHT = window.winfo_screenheight()
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)

def home_screen():
    menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Evolution Simulator', theme=pygame_menu.themes.THEME_DARK)
    menu.add_button('Sign-Up', sign_in)
    menu.add_button('Log In', log_in)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)

def sign_in():
    menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Sign In', theme=pygame_menu.themes.THEME_DARK)
    menu.add_button('Sign-Up', sign_in)
    menu.add_button('Log In', log_in)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)

def log_in():
    print("Log In")

home_screen()