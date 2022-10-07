import pygame
import pygame_menu
from pygame.locals import *

from tkinter import *
window = Tk()

pygame.init()
SCREEN_WIDTH = window.winfo_screenwidth()
SCREEN_HEIGHT = window.winfo_screenheight()


class welcome_screen():
    def __init__(self):
        SCREEN_WIDTH = window.winfo_screenwidth()
        SCREEN_HEIGHT = window.winfo_screenheight()
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Evolution Simulator', theme=pygame_menu.themes.THEME_DARK)
        self.menu.add_label('Evolution Simulator')
        self.menu.add_button('Sign-Up', self.sign_in)
        self.menu.add_button('Log In', self.log_in)
        self.menu.add_button('Quit', pygame_menu.events.EXIT)
        self.menu.mainloop(surface)

    def sign_in(self):
        print("Sign Up")

    def log_in(self):
        print("Log In")

welcome_screen()