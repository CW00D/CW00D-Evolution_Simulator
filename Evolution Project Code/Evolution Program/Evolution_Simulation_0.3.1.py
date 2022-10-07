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

class welcome_screen():
    def __init__(self):
        SCREEN_WIDTH = window.winfo_screenwidth()
        SCREEN_HEIGHT = window.winfo_screenheight()
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Evolution Simulator', theme=pygame_menu.themes.THEME_DARK)
        menu.add_label('Evolution Simulatior')
        menu.add_button('Sign-Up', self.sign_in)
        menu.add_button('Log In', self.log_in)
        menu.add_button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(surface)

    def sign_in(self):
        signup_screen()

    def log_in(self):
        print("Log In")

class signup_screen():
    def __init__(self):
        SCREEN_WIDTH = window.winfo_screenwidth()
        SCREEN_HEIGHT = window.winfo_screenheight()
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Sign Up', theme=pygame_menu.themes.THEME_DARK)
        menu.add_text_input('Name:', default='')
        menu.add_text_input('Username:', default='')
        menu.add_text_input('Password:', default='')
        menu.add_text_input('Repeat Password:', default='')
        menu.add_button('Sign Up', self.sign_up)
        menu.add_button('Back', self.welcome_screen)
        menu.mainloop(surface)

    def welcome_screen(self):
        welcome_screen()

    def sign_up(self):
        print("Signing Up")

welcome_screen()
