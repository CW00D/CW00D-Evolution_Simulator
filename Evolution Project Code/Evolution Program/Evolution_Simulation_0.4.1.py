import pygame
import pygame_menu
from pygame.locals import *
from tkinter import *
window = Tk()
pygame.init()
SCREEN_WIDTH = window.winfo_screenwidth()
SCREEN_HEIGHT = window.winfo_screenheight()

from Evolution_simulator_schema_v2 import User, Simulation, Species, SpeciesHistory, Organism, Map, Food
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
engine = create_engine('sqlite:///evolution_simulator.db', echo=False)
session = sessionmaker(bind=engine)()

class Program():
    def __init__(self):
        self.user_logged_in = None
        Welcome_screen()

class Welcome_screen():
    def __init__(self):
        SCREEN_WIDTH = window.winfo_screenwidth()
        SCREEN_HEIGHT = window.winfo_screenheight()
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Evolution Simulator', theme=pygame_menu.themes.THEME_DARK)
        self.menu.add_label('Evolution Simulatior')
        self.menu.add_button('Sign-Up', self.sign_in)
        self.menu.add_button('Log In', self.log_in)
        self.menu.add_button('Quit', pygame_menu.events.EXIT)
        self.menu.mainloop(surface)

    def sign_in(self):
        Signup_screen()

    def log_in(self):
        Login_screen()

class Signup_screen():
    def __init__(self):
        SCREEN_WIDTH = window.winfo_screenwidth()
        SCREEN_HEIGHT = window.winfo_screenheight()
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, "Sign Up", theme=pygame_menu.themes.THEME_DARK)
        self.input_name = self.menu.add_text_input("Name:  ", default="")
        self.input_username = self.menu.add_text_input("Username:  ", default="")
        self.input_password = self.menu.add_text_input("Password:  ", default="", password=True)
        self.input_repeat_password = self.menu.add_text_input("Repeat Password:   ", default="", password=True)
        self.menu.add_button("Sign Up", self.sign_up)
        self.menu.add_button("Back", self.welcome_screen)
        self.menu.mainloop(surface)

    def welcome_screen(self):
        Welcome_screen()

    def home_screen(self):
        print("Home Screen")

    def sign_up(self):
        data = self.menu.get_input_data(recursive=False)
        input_name = data[self.input_name.get_id()]
        input_username = data[self.input_username.get_id()]
        input_password = data[self.input_password.get_id()]
        input_repeat_password = data[self.input_repeat_password.get_id()]
        
        self.validate_data(input_name, input_username, input_password, input_repeat_password)

    def validate_data(self, name, username, password, repeat_password):
        usernames = session.query(User).filter(User.username == username).all()
        if len(usernames) != 0:
            Signup_screen()
        if password != repeat_password:
            Signup_screen()        
        self.add_data_to_database(name, username, password, repeat_password)

    def add_data_to_database(self, name, username, password, repeat_password):
        user = User(name=name, username=username, password=password)
        session.add(user)
        session.commit()  
        Program.user_logged_in = user     
        self.home_screen()

class Login_screen():
    def __init__(self):
        SCREEN_WIDTH = window.winfo_screenwidth()
        SCREEN_HEIGHT = window.winfo_screenheight()
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, "Log In", theme=pygame_menu.themes.THEME_DARK)
        self.username = self.menu.add_text_input("Username:  ", default="")
        self.password = self.menu.add_text_input("Password:  ", default="", password=True)
        self.menu.add_button("Log In", self.log_in)
        self.menu.add_button("Back", self.welcome_screen)
        self.menu.mainloop(surface)

    def welcome_screen(self):
        Welcome_screen()
    
    def home_screen(self):
        print("Home Screen")

    def log_in(self):
        data = self.menu.get_input_data(recursive=False)
        username = data[self.username.get_id()]
        password = data[self.password.get_id()]
        user = session.query(User).filter(User.username == username).one_or_none()
        if user == None:
            Login_screen()
        if user.password  == password:
            Program.user_logged_in = user
            self.home_screen()
        else:
            Login_screen()

Program()