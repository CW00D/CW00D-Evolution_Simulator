import random

import pygame
import pygame_menu
from pygame.locals import *
from tkinter import *
window = Tk()
pygame.init()

from Evolution_simulator_schema_v2 import User, Simulation, Species, SpeciesHistory, Organism, Map, Food, Tile
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, date
engine = create_engine("sqlite:///evolution_simulator.db", echo=False)
session = sessionmaker(bind=engine)()

BLACK = (38,38,38)
WHITE = (200,200,200)
GREEN = (153,186,56)

class Program():
    def __init__(self):
        self.user_logged_in = None
        self.current_simulation = None
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
        Saved_Simulations_screen()

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

    def generate_simulation(self):
        Simulation_Screen()

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
        simulation_name = "Simulation_" + str(date.today())
        date_created = datetime.now()
        length_of_turn = random.randint(5,20)
        starting_number_of_organisms = random.randint(50,200)
        starting_number_of_species = random.randint(5,20)
        
        map_size = random.randint(25,200)
        number_of_food_sources = random.randint(10,50)
        number_of_water_sources = random.randint(10,50)
        average_temperature = random.randint(0, 45)
        temperature_range = random.randint(0, 20)

        simulation = Simulation(simulation_name=simulation_name, date_last_used=date_created, current_turn=0, length_of_turn=length_of_turn, starting_number_of_organisms=starting_number_of_organisms, starting_number_of_species=starting_number_of_species, current_number_of_organisms=starting_number_of_organisms, current_number_of_species=starting_number_of_species, user_id=Program.user_logged_in.id, user_relationship=Program.user_logged_in)
        session.add(simulation)
        session.commit()  

        map_to_add = Map(map_size=map_size, number_of_food_sources=number_of_food_sources, number_of_water_sources=number_of_water_sources, average_temperature=average_temperature, temperature_range=temperature_range, simulation_id=simulation.id, simulation_relationship=simulation)
        session.add(map_to_add)
        session.commit()  

        Program.current_simulation = simulation
        
        self.generate_simulation()

class Custom_Detail_Entry_screen():
    def __init__(self):
        SCREEN_WIDTH = window.winfo_screenwidth()
        SCREEN_HEIGHT = window.winfo_screenheight()
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, "Custom Detail Entry", theme=pygame_menu.themes.THEME_DARK)
        self.menu.add_label("Simulation Details")
        self.simulation_name = self.menu.add_text_input("Name of Simulation:  ", default="Simulation_")
        self.length_of_turn = self.menu.add_text_input("Length of Turn:  ", default="10")
        self.starting_number_of_organisms = self.menu.add_text_input("Starting Number of Organisms:  ", default="100")
        self.starting_number_of_species = self.menu.add_text_input("Starting Number of Species:  ", default="10")
        self.menu.add_label("")
        self.menu.add_label("Map Details")
        self.map_size = self.menu.add_text_input("Map Size:  ", default="10")
        self.number_of_food_sources = self.menu.add_text_input("Number of Food Sources:  ", default="5")
        self.number_of_water_sources = self.menu.add_text_input("Number of Water Sources:  ", default="5")
        self.average_temperature = self.menu.add_text_input("Average Temperature:  ", default="5")
        self.temperature_range = self.menu.add_text_input("Temperature Range:  ", default="5")
        self.menu.add_label("")
        self.menu.add_button("Generate", self.collect_input_data)
        self.menu.add_button("Back", self.home_screen)
        self.menu.mainloop(surface)

    def home_screen(self):
        Home_screen()

    def generating_screen(self):
        Simulation_Screen()

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

        Program.current_simulation = simulation
        self.generating_screen()

class Saved_Simulations_screen():
    def __init__(self):
        SCREEN_WIDTH = window.winfo_screenwidth()
        SCREEN_HEIGHT = window.winfo_screenheight()
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, "Saved Simulations", theme=pygame_menu.themes.THEME_DARK)
        user_simulations = session.query(Simulation).filter(Simulation.user_relationship == Program.user_logged_in).order_by(Simulation.date_last_used.desc()).all()
        if len(user_simulations) == 0:
            self.menu.add_label("You have no saved simulations")
        else:
            self.menu.add_button(user_simulations[0].simulation_name, self.load_simulation_1)
            try:
                self.menu.add_button(user_simulations[1].simulation_name, self.load_simulation_2)
            except:
                pass
            try:    
                self.menu.add_button(user_simulations[2].simulation_name, self.load_simulation_3)
            except:
                pass
        self.menu.add_button("Back", self.home_screen)
        self.menu.mainloop(surface)

    def home_screen(self):
        Home_screen()

    def load_simulation_1(self):
        simulation = session.query(Simulation).filter(Simulation.user_relationship == Program.user_logged_in).order_by(Simulation.date_last_used.desc()).first()
        simulation.date_last_used = datetime.now()
        session.commit()
        Program.current_simulation=simulation
        self.generate()
    
    def load_simulation_2(self):
        simulations = session.query(Simulation).filter(Simulation.user_relationship == Program.user_logged_in).order_by(Simulation.date_last_used.desc()).all()
        simulation = simulations[1]
        simulation.date_last_used = datetime.now()
        session.commit()
        Program.current_simulation=simulation
        self.generate()

    def load_simulation_3(self):
        simulations = session.query(Simulation).filter(Simulation.user_relationship == Program.user_logged_in).order_by(Simulation.date_last_used.desc()).all()
        simulation = simulations[2]
        simulation.date_last_used = datetime.now()
        session.commit()
        Program.current_simulation=simulation
        self.generate()

    def generate(self):
        Simulation_Screen()

class Simulation_Screen():
    def __init__(self):
        self.simulation = Program.current_simulation
        self.simulation_map = self.simulation.map_relationship[0]
        self.map_size = self.simulation_map.map_size

        self.screen_width = window.winfo_screenwidth()
        self.screen_height = window.winfo_screenheight()
        self.surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.surface.fill(BLACK)

        self.surface_height = int(self.screen_height-100) 
        self.block_size = int(self.surface_height/self.simulation_map.map_size)
        self.surface_width = int(self.block_size*self.simulation_map.map_size)
        
        surface=self.surface
        self.simulation_surface = pygame.surface.Surface((self.surface_width, self.surface_height))
        self.simulation_surface.fill(BLACK)

        self.block_size = int(self.surface_height/self.simulation_map.map_size)

        self.pause_button_position = [100,300]
        self.save_button_position = [100, 370]
        self.quit_button_position = [100,440]
        self.analysis_button_position = [1300,300]

        smallfont = pygame.font.SysFont("Corbel",40) 
        self.pause_text = smallfont.render("Pause" , True , WHITE) 
        self.save_text = smallfont.render("Save" , True , WHITE) 
        self.quit_text = smallfont.render("Quit", True, WHITE)
        self.analysis_text = smallfont.render("Analysis", True, WHITE)

        self.tile_array = [[None]*self.simulation_map.map_size]*self.simulation_map.map_size
        self.tile_array = [[None for i in range(self.map_size)] for j in range(self.map_size)]

        if len(self.simulation.tile_relationship) == 0:
            self.set_up_grid()
        #    self.position_water()
        #    self.position_veg()
        #    self.position_meat()
        self.create_tiles()
        self.draw_buttons()
        self.draw_tiles()


        while True:
            mouse = pygame.mouse.get_pos() 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if self.pause_button_position[0] <= mouse[0] <= self.pause_button_position[0]+140 and self.pause_button_position[1] <= mouse[1] <= self.pause_button_position[1]+40: 
                        self.pause()

                    if self.save_button_position[0] <= mouse[0] <= self.save_button_position[0]+140 and self.save_button_position[1] <= mouse[1] <= self.save_button_position[1]+40: 
                        self.save()

                    if self.quit_button_position[0] <= mouse[0] <= self.quit_button_position[0]+140 and self.quit_button_position[1] <= mouse[1] <= self.quit_button_position[1]+40: 
                        self.quit_simulation() 

                    if self.analysis_button_position[0] <= mouse[0] <= self.analysis_button_position[0]+180 and self.analysis_button_position[1] <= mouse[1] <= self.analysis_button_position[1]+40: 
                        self.analysis()                      

            pygame.display.update()

    def set_up_grid(self):
        for x in range(self.map_size):
            for y in range(self.map_size):
                tile = Tile(x_coordinate=x, y_coordinate=y, x_position=x*self.block_size, y_position=y*self.block_size, tile_type=None, simulation_relationship=self.simulation)
                session.add(tile)
                session.commit()

    def position_water(self):
        print("Positioning Water")
    
    def position_veg(self):
        print("Positioning Veg")

    def position_meat(self):
        print("Positioning Meat")

    def create_tiles(self):
        for x in range(self.map_size):
            for y in range(self.map_size):
                print(self.tile_array[x][y])
                self.tile_array[x][y] = Simulation_Tile(self.surface, self.simulation_surface, self.block_size, x*self.block_size, y*self.block_size, self.screen_width)
        print(self.tile_array[0][0].x_position)

    def draw_tiles(self):
        for x in range(self.map_size):
            for y in range(self.map_size):
                self.tile_array[x][y].draw_tile()

    def draw_buttons(self):
        pygame.draw.rect(self.surface,WHITE,[self.pause_button_position[0],self.pause_button_position[1],140,40],1) 
        self.surface.blit(self.pause_text , (self.pause_button_position[0]+30,self.pause_button_position[1])) 

        pygame.draw.rect(self.surface,WHITE,[self.save_button_position[0],self.save_button_position[1],140,40],1) 
        self.surface.blit(self.save_text , (self.save_button_position[0]+30,self.save_button_position[1])) 

        pygame.draw.rect(self.surface,WHITE,[self.quit_button_position[0],self.quit_button_position[1],140,40],1) 
        self.surface.blit(self.quit_text , (self.quit_button_position[0]+30,self.quit_button_position[1]))

        pygame.draw.rect(self.surface,WHITE,[self.analysis_button_position[0],self.analysis_button_position[1],180,40],1) 
        self.surface.blit(self.analysis_text , (self.analysis_button_position[0]+30,self.analysis_button_position[1]))

    def pause(self):
        print("Pause")

    def save(self):
        print("Save")

    def quit_simulation(self):
        Program.current_simulation = None
        Home_screen()

    def analysis(self):
        print("Analysis")

class Simulation_Tile:
    def __init__(self, surface, simulation_surface, block_size, x_position, y_position, screen_width):
        self.surface = surface
        self.simulation_surface = simulation_surface
        self.block_size = block_size
        self.x_position = x_position
        self.y_position = y_position
        self.screen_width = screen_width
        self.image = "Grass.png"
        self.tile_type = "Blank"

    def draw_tile(self):
        image_to_draw = pygame.image.load(self.image).convert_alpha()
        scaled_image = pygame.transform.scale(image_to_draw, (self.block_size, self.block_size))
        self.simulation_surface.blit(scaled_image, pygame.Rect(self.x_position, self.y_position, self.block_size, self.block_size).topleft)
        self.surface.blit(self.simulation_surface, (int(self.screen_width*(1/5)),50))

Program()