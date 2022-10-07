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
engine = create_engine("sqlite:///evolution_simulator.db", echo=False)
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
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, "Evolution Simulator", theme=pygame_menu.themes.THEME_DARK)
        self.menu.add_label("Evolution Simulatior")
        self.menu.add_button("Sign-Up", self.sign_in)
        self.menu.add_button("Log In", self.log_in)
        self.menu.add_button("Quit", pygame_menu.events.EXIT)
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
        self.menu.add_label("")
        self.menu.add_button("Sign Up", self.sign_up)
        self.menu.add_button("Back", self.welcome_screen)
        self.menu.mainloop(surface)

    def welcome_screen(self):
        Welcome_screen()

    def home_screen(self):
        Home_screen()

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
        Home_screen()

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

class Home_screen():
    def __init__(self):
        SCREEN_WIDTH = window.winfo_screenwidth()
        SCREEN_HEIGHT = window.winfo_screenheight()
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, "Home", theme=pygame_menu.themes.THEME_DARK)
        self.menu.add_label("Welcome back " + Program.user_logged_in.name)
        self.menu.add_button("New Simulation", self.new_simulation_screen)
        self.menu.add_button("Saved Simulations", self.saved_simulations_screen)
        self.menu.add_button("Log Out", self.log_out)
        self.menu.mainloop(surface)

    def welcome_screen(self):
        Welcome_screen()

    def new_simulation_screen(self):
        New_simulation_screen()

    def saved_simulations_screen(self):
        print("saved simulations screen")

    def log_out(self):
        Program.user_logged_in = None
        self.welcome_screen()

class New_simulation_screen():
    def __init__(self):
        self.current_generation_type = "Random"
        SCREEN_WIDTH = window.winfo_screenwidth()
        SCREEN_HEIGHT = window.winfo_screenheight()
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, "Simulation Generation", theme=pygame_menu.themes.THEME_DARK)
        self.menu.add_selector("Simulation Variables:", [("Randomized", 1), ("    Custom    ", 2)], onchange=self.change_input)
        self.menu.add_button("Create Simulation", self.create_simulation)
        self.menu.add_button("Back to Home Screen", self.home_screen)
        self.menu.mainloop(surface)

    def home_screen(self):
        Home_screen()

    def change_input(self, val_1, val_2):
        if val_2 == 1:
            self.current_generation_type = "Random"
        if val_2 == 2:
            self.current_generation_type = "Custom"

    def create_simulation(self):
        if self.current_generation_type == "Custom":
            Custom_Detail_Entry_screen()
        elif self.current_generation_type == "Random":
            self.randomly_generate()

    def randomly_generate(self):
        print("Randomly Generate")

class Custom_Detail_Entry_screen():
    def __init__(self):
        SCREEN_WIDTH = window.winfo_screenwidth()
        SCREEN_HEIGHT = window.winfo_screenheight()
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, "Custom Detail Entry", theme=pygame_menu.themes.THEME_DARK)
        self.menu.add_label("Simulation Details")
        self.simulation_name = self.menu.add_text_input("Name of Simulation:  ", default="")
        self.length_of_turn = self.menu.add_text_input("Length of Turn:  ", default="10")
        self.starting_number_of_organisms = self.menu.add_text_input("Starting Number of Organisms:  ", default="100")
        self.starting_number_of_species = self.menu.add_text_input("Starting Number of Species:  ", default="10")
        self.menu.add_label("")
        self.menu.add_label("Map Details")
        self.map_size = self.menu.add_text_input("Map Size:  ", default="100")
        self.number_of_food_sources = self.menu.add_text_input("Number of Food Sources:  ", default="25")
        self.number_of_water_sources = self.menu.add_text_input("Number of Water Sources:  ", default="25")
        self.average_temperature = self.menu.add_text_input("Average Temperature:  ", default="25")
        self.temperature_range = self.menu.add_text_input("Temperature Range:  ", default="25")
        self.menu.add_label("")
        self.menu.add_button("Generate", self.collect_input_data)
        self.menu.add_button("Back", self.home_screen)
        self.menu.mainloop(surface)

    def home_screen(self):
        Home_screen()

    def generating_screen(self):
        print("Generating")

    def collect_input_data(self):
        data = self.menu.get_input_data(recursive=False)
        simulation_name = data[self.simulation_name.get_id()]
        date_created = datetime.now()
        length_of_turn = data[self.length_of_turn.get_id()]
        starting_number_of_organisms = data[self.starting_number_of_organisms.get_id()]
        starting_number_of_species = data[self.starting_number_of_species.get_id()]
        
        map_size = data[self.map_size.get_id()]
        number_of_food_sources = data[self.number_of_food_sources.get_id()]
        number_of_water_sources = data[self.number_of_water_sources.get_id()]
        average_temperature = data[self.average_temperature.get_id()]
        temperature_range = data[self.temperature_range.get_id()]

        self.generate(simulation_name, date_created, length_of_turn, starting_number_of_organisms, starting_number_of_species, map_size, number_of_food_sources, number_of_water_sources, average_temperature, temperature_range)
    
    def generate(self, simulation_name, date_created, lenth_of_turn, starting_number_of_organisms, starting_number_of_species, map_size, number_of_food_sources, number_of_water_sources, average_temperature, temperature_range):
        current_simulations = session.query(Simulation).filter(Simulation.user_relationship == Program.user_logged_in).order_by(Simulation.date_last_used.desc()).all()
        if len(current_simulations) >= 3:
            session.delete(current_simulations[-1])
        simulation = Simulation(simulation_name=simulation_name, date_last_used=date_created, current_turn=0, length_of_turn=lenth_of_turn, starting_number_of_organisms=starting_number_of_organisms, starting_number_of_species=starting_number_of_species, current_number_of_organisms=starting_number_of_organisms, current_number_of_species=starting_number_of_species, user_id=Program.user_logged_in.id, user_relationship=Program.user_logged_in)
        map_to_add = Map(map_size=map_size, number_of_food_sources=number_of_food_sources, number_of_water_sources=number_of_water_sources, average_temperature=average_temperature, temperature_range=temperature_range, simulation_id=simulation.id, simulation_relationship=simulation)
        session.add(simulation)
        session.commit()

        self.generating_screen()

Program()