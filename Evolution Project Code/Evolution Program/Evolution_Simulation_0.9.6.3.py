import random
import pygame
import pygame_menu
import time
from pygame.locals import *
from tkinter import *
window = Tk()
pygame.init()

from Evolution_simulator_schema_v4 import User, Simulation, Species, SpeciesHistory, Organism, Map, Food, Tile
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
        self.current_generation_type = "Custom"
        SCREEN_WIDTH = window.winfo_screenwidth()
        SCREEN_HEIGHT = window.winfo_screenheight()
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, "Simulation Generation", theme=pygame_menu.themes.THEME_DARK)
        self.menu.add_selector("Simulation Variables:", [("    Custom    ", 1), ("Randomized", 2)], onchange=self.change_input)
        self.menu.add_button("Create Simulation", self.create_simulation)
        self.menu.add_button("Back to Home Screen", self.home_screen)
        self.menu.mainloop(surface)

    def home_screen(self):
        Home_screen()

    def generate_simulation(self):
        Simulation_Screen()

    def change_input(self, val_1, val_2):
        if val_2 == 1:
            self.current_generation_type = "Custom"
        if val_2 == 2:
            self.current_generation_type = "Random"

    def create_simulation(self):
        if self.current_generation_type == "Custom":
            Custom_Detail_Entry_screen()
        elif self.current_generation_type == "Random":
            self.randomly_generate()

    def randomly_generate(self):
        simulation_name = "Simulation_" + str(date.today())
        date_created = datetime.now()
        length_of_turn = random.randint(5,20)
        starting_number_of_organisms = random.randint(5,20)
        starting_number_of_species = random.randint(2,10)
        
        map_size = random.randint(5,30)
        number_of_food_sources = random.randint(2,10)
        meat_to_veg_ratio = str(random.randint(1,5))+":"+str(random.randint(1,5))
        number_of_water_sources = random.randint(2,10)

        simulation = Simulation(simulation_name=simulation_name, date_last_used=date_created, current_turn=0, length_of_turn=length_of_turn, starting_number_of_organisms=starting_number_of_organisms, starting_number_of_species=starting_number_of_species, current_number_of_organisms=starting_number_of_organisms, current_number_of_species=starting_number_of_species, user_id=Program.user_logged_in.id, user_relationship=Program.user_logged_in)
        session.add(simulation)
        session.commit()  

        map_to_add = Map(map_size=map_size, number_of_food_sources=number_of_food_sources, meat_to_veg_ratio=meat_to_veg_ratio, number_of_water_sources=number_of_water_sources, simulation_id=simulation.id, simulation_relationship=simulation)
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
        self.starting_number_of_organisms = self.menu.add_text_input("Starting Number of Organisms:  ", default="10")
        self.starting_number_of_species = self.menu.add_text_input("Starting Number of Species:  ", default="3")
        self.menu.add_label("")
        self.menu.add_label("Map Details")
        self.map_size = self.menu.add_text_input("Map Size:  ", default="10")
        self.number_of_food_sources = self.menu.add_text_input("Number of Food Sources:  ", default="10")
        self.meat_to_veg_ratio = self.menu.add_text_input("Meat to Veg Ratio:  ", default="1:3")
        self.number_of_water_sources = self.menu.add_text_input("Number of Water Sources:  ", default="5")
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
        meat_to_veg_ratio = data[self.meat_to_veg_ratio.get_id()]
        number_of_water_sources = data[self.number_of_water_sources.get_id()]

        self.generate(simulation_name, date_created, length_of_turn, starting_number_of_organisms, starting_number_of_species, map_size, number_of_food_sources, meat_to_veg_ratio, number_of_water_sources)
    
    def generate(self, simulation_name, date_created, lenth_of_turn, starting_number_of_organisms, starting_number_of_species, map_size, number_of_food_sources, meat_to_veg_ratio, number_of_water_sources):
        current_simulations = session.query(Simulation).filter(Simulation.user_relationship == Program.user_logged_in).order_by(Simulation.date_last_used.desc()).all()
        if len(current_simulations) >= 3:
            session.delete(current_simulations[-1])
        simulation = Simulation(simulation_name=simulation_name, date_last_used=date_created, current_turn=0, length_of_turn=lenth_of_turn, starting_number_of_organisms=starting_number_of_organisms, starting_number_of_species=starting_number_of_species, current_number_of_organisms=starting_number_of_organisms, current_number_of_species=starting_number_of_species, user_id=Program.user_logged_in.id, user_relationship=Program.user_logged_in)
        map_to_add = Map(map_size=map_size, number_of_food_sources=number_of_food_sources, meat_to_veg_ratio=meat_to_veg_ratio, number_of_water_sources=number_of_water_sources, simulation_id=simulation.id, simulation_relationship=simulation)
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
        self.simulation_state = 0
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
        self.start_text = smallfont.render("Start" , True , WHITE) 
        self.pause_text = smallfont.render("Pause" , True , WHITE) 
        self.play_text = smallfont.render("Play" , True , WHITE)
        self.save_text = smallfont.render("Save" , True , WHITE) 
        self.quit_text = smallfont.render("Quit", True, WHITE)
        self.analysis_text = smallfont.render("Analysis", True, WHITE)

        self.start_time = time.time()
        self.interval = 1.0/self.simulation.length_of_turn
        self.tick = self.interval / 50.0
        self.count = 0

        self.tile_array = [[None for i in range(self.map_size)] for j in range(self.map_size)]

        self.organisms = []
        self.organism_tiles = []

        if len(self.simulation.tile_relationship) == 0:
            self.set_up_grid()
            self.position_water()
            self.position_veg_and_fruit()
            self.position_meat()
            self.create_species()
            self.create_organisms()
        self.create_tiles()
        self.find_tile_neighbours()
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
                        if self.simulation_state==0:
                            self.start()
                        elif self.simulation_state==1:    
                            self.pause()
                        elif self.simulation_state==2:
                            self.play()

                    if self.save_button_position[0] <= mouse[0] <= self.save_button_position[0]+140 and self.save_button_position[1] <= mouse[1] <= self.save_button_position[1]+40: 
                        self.save()

                    if self.quit_button_position[0] <= mouse[0] <= self.quit_button_position[0]+140 and self.quit_button_position[1] <= mouse[1] <= self.quit_button_position[1]+40: 
                        self.quit_simulation() 

                    if self.analysis_button_position[0] <= mouse[0] <= self.analysis_button_position[0]+180 and self.analysis_button_position[1] <= mouse[1] <= self.analysis_button_position[1]+40: 
                        self.analysis()                      
            pygame.display.update()

        
            if self.simulation_state == 1:
                self.organism_tiles = []
                self.move_organisms()
                self.tile_array = [[None for i in range(self.map_size)] for j in range(self.map_size)]
                self.create_tiles()
                self.draw_tiles()
                self.find_tile_neighbours()
                for tile in self.organism_tiles:
                    self.check_area_around(tile)
                self.count += 1
        
    def set_up_grid(self):
        for x in range(self.map_size):
            for y in range(self.map_size):
                tile = Tile(x_coordinate=x, y_coordinate=y, x_position=x*self.block_size, y_position=y*self.block_size, tile_type="Blank", simulation_id=self.simulation.id, simulation_relationship=self.simulation, food_id=None, food_relationship=None, organism_id=None, organism_relationship=None)
                session.add(tile)
                session.commit()

    def position_water(self):
        for i in range(self.simulation_map.number_of_water_sources):
            x = random.randint(0, self.map_size-1)
            y = random.randint(0, self.map_size-1)
            tile_at_xy = session.query(Tile).filter(Tile.x_coordinate == x).filter(Tile.y_coordinate == y).filter(Tile.simulation_relationship == Program.current_simulation).one()
            while tile_at_xy.tile_type != "Blank":
                x = random.randint(0, self.map_size-1)
                y = random.randint(0, self.map_size-1)
                tile_at_xy = session.query(Tile).filter(Tile.x_coordinate == x).filter(Tile.y_coordinate == y).filter(Tile.simulation_relationship == Program.current_simulation).one()
            tile_at_xy.tile_type = "Water"
            session.commit()
    
    def position_veg_and_fruit(self):
        proportion_of_veg = int(self.simulation_map.meat_to_veg_ratio.split(":")[1])/(int(self.simulation_map.meat_to_veg_ratio.split(":")[0])+int(self.simulation_map.meat_to_veg_ratio.split(":")[1]))
        for i in range(round(self.simulation_map.number_of_food_sources*proportion_of_veg)):
            x = random.randint(0, self.map_size-1)
            y = random.randint(0, self.map_size-1)
            tile_at_xy = session.query(Tile).filter(Tile.x_coordinate == x).filter(Tile.y_coordinate == y).filter(Tile.simulation_relationship == Program.current_simulation).one()
            while tile_at_xy.tile_type != "Blank":
                x = random.randint(0, self.map_size-1)
                y = random.randint(0, self.map_size-1)
                tile_at_xy = session.query(Tile).filter(Tile.x_coordinate == x).filter(Tile.y_coordinate == y).filter(Tile.simulation_relationship == Program.current_simulation).one()
            if random.randint(0,10) <= 5:
                tile_at_xy.tile_type = "Veg"
                veg_item = Food(food_type="Veg", nutritional_value="ccdccaaadc", consumption_code="abbcabcbdb", x_coordinate=x, y_coordinate=y, map_id=self.simulation_map.id, map_relationship=self.simulation_map, tile_relationship=tile_at_xy)
                session.add(veg_item)
                tile_at_xy.food_relationship=veg_item
                tile_at_xy.food_id=veg_item.id
            else:
                tile_at_xy.tile_type = "Fruit"
                fruit_item = Food(food_type="Fruit", nutritional_value="ccbccaaabc", consumption_code = "accbacbcdc", x_coordinate=x, y_coordinate=y, map_id=self.simulation_map.id, map_relationship=self.simulation_map, tile_relationship=tile_at_xy)
                session.add(fruit_item)
                tile_at_xy.food_relationship=fruit_item
                tile_at_xy.food_id=fruit_item.id
            session.commit()

    def position_meat(self):
        proportion_of_meat = int(self.simulation_map.meat_to_veg_ratio.split(":")[0])/(int(self.simulation_map.meat_to_veg_ratio.split(":")[0])+int(self.simulation_map.meat_to_veg_ratio.split(":")[1]))
        for i in range(round(self.simulation_map.number_of_food_sources*proportion_of_meat)):
            x = random.randint(0, self.map_size-1)
            y = random.randint(0, self.map_size-1)
            tile_at_xy = session.query(Tile).filter(Tile.x_coordinate == x).filter(Tile.y_coordinate == y).filter(Tile.simulation_relationship == self.simulation).one()
            while tile_at_xy.tile_type != "Blank":
                x = random.randint(0, self.map_size-1)
                y = random.randint(0, self.map_size-1)
                tile_at_xy = session.query(Tile).filter(Tile.x_coordinate == x).filter(Tile.y_coordinate == y).filter(Tile.simulation_relationship == self.simulation).one()
            tile_at_xy.tile_type = "Meat"
            meat_item = Food(food_type="Meat", nutritional_value="ddbddabadc", consumption_code="cdccdddccd", x_coordinate=x, y_coordinate=y, map_id=self.simulation_map.id, map_relationship=self.simulation_map, tile_relationship=tile_at_xy)
            tile_at_xy.food_relationship=meat_item
            tile_at_xy.food_id=meat_item.id
            session.add(meat_item)
            session.commit()

    def create_species(self):#add new chromosome structures + change the way the reproduction code is created
        standard_chromosomes = ["abbaca,aabab|baadb,aaaa,abc|abccc","bbadbc,bbbb,abaa|a,bbbb,adc|ac,ac"]
        for species in range(self.simulation.starting_number_of_species):
            new_species_chromosome = standard_chromosomes[random.randint(0,len(standard_chromosomes)-1)]
            tag_section = new_species_chromosome.split("|")[0]
            control_section = new_species_chromosome.split("|")[1]
            exchange_section = new_species_chromosome.split("|")[2]
            new_species_chromosome = self.randomize_chromosome(tag_section, control_section, exchange_section)
            tag_section = new_species_chromosome.split("|")[0]
            control_section = new_species_chromosome.split("|")[1]
            exchange_section = new_species_chromosome.split("|")[2]
            new_species_colour = self.find_colour(tag_section, control_section, exchange_section)
            new_species_reproduction_code = control_section.split(",")[1]
            new_species = Species(average_chromosome=new_species_chromosome, average_species_colour=new_species_colour, average_reproduction_code=new_species_reproduction_code, simulation_id=self.simulation.id, simulation_relationship=self.simulation)
            session.add(new_species)
            session.commit()

    def create_organisms(self):
        species = session.query(Species).filter(Species.simulation_relationship==self.simulation).all()
        for current_species in species:
            for i in range(int(self.simulation.starting_number_of_organisms/self.simulation.starting_number_of_species)):
                x = random.randint(0, self.map_size-1)
                y = random.randint(0, self.map_size-1)
                tile_at_xy = session.query(Tile).filter(Tile.x_coordinate == x).filter(Tile.y_coordinate == y).filter(Tile.simulation_relationship == Program.current_simulation).one()
                while tile_at_xy.tile_type != "Blank":
                    x = random.randint(0, self.map_size-1)
                    y = random.randint(0, self.map_size-1)
                    tile_at_xy = session.query(Tile).filter(Tile.x_coordinate == x).filter(Tile.y_coordinate == y).filter(Tile.simulation_relationship == Program.current_simulation).one()
                tile_at_xy.tile_type = "Organism"
                new_organism = Organism(chromosome=current_species.average_chromosome, reservoir="abcd", colour=current_species.average_species_colour, reproduction_code=current_species.average_reproduction_code, x_position=x, y_position=y, species_id=current_species.id, species_relationship=current_species, simulation_id=self.simulation.id, simulation_relationship=self.simulation)
                session.add(new_organism)
                tile_at_xy.organism_id = new_organism.id
                tile_at_xy.organism_relationship = new_organism
                session.commit()

    def randomize_chromosome(self, tag_section, control_section, exchange_section):
        new_chromosome = ""
        for character in list(tag_section):
            if character == ",":
                new_chromosome+=","
            else:
                random_value = random.randint(0,10)
                if random_value<8:
                    new_chromosome+=character                
                elif character == "a":
                    available_letters = ["b","c","d"]
                    new_chromosome+=available_letters[random_value-8]
                elif character == "b":
                    available_letters = ["a","c","d"]
                    new_chromosome+=available_letters[random_value-8]   
                elif character == "c":
                    available_letters = ["a","b","d"]
                    new_chromosome+=available_letters[random_value-8] 
                elif character == "d":
                    available_letters = ["a","b","c"]
                    new_chromosome+=available_letters[random_value-8] 
        new_chromosome+="|"
        for character in list(control_section):
            if character == ",":
                new_chromosome+=","
            else:
                random_value = random.randint(0,20)
                if random_value<16:
                    new_chromosome+=character                
                elif character == "a":
                    available_letters = ["b","b","d","c","#"]
                    new_chromosome+=available_letters[random_value-16]
                elif character == "b":
                    available_letters = ["c","c","a","d","#"]
                    new_chromosome+=available_letters[random_value-16]   
                elif character == "c":
                    available_letters = ["d","d","b","a","#"]
                    new_chromosome+=available_letters[random_value-16] 
                elif character == "d":
                    available_letters = ["a","a","c","b","#"]
                    new_chromosome+=available_letters[random_value-16] 
                elif character == "#":
                    available_letters = ["a","b","c","d","#"]
                    new_chromosome+=available_letters[random_value-16] 
        new_chromosome+="|"
        for character in list(exchange_section):
            if character == ",":
                new_chromosome+=","
            else:
                random_value = random.randint(0,20)
                if random_value<16:
                    new_chromosome+=character                
                elif character == "a":
                    available_letters = ["b","b","d","c","#"]
                    new_chromosome+=available_letters[random_value-16]
                elif character == "b":
                    available_letters = ["c","c","a","d","#"]
                    new_chromosome+=available_letters[random_value-16]   
                elif character == "c":
                    available_letters = ["d","d","b","a","#"]
                    new_chromosome+=available_letters[random_value-16] 
                elif character == "d":
                    available_letters = ["a","a","c","b","#"]
                    new_chromosome+=available_letters[random_value-16] 
                elif character == "#":
                    available_letters = ["a","b","c","d","#"]
                    new_chromosome+=available_letters[random_value-16] 
        return(new_chromosome)

    def find_colour(self, tag_section, control_section, exchange_section):
        R_value = 0
        for value in list(tag_section):
            if value != ",":
                R_value += ord(value)
        R_value = R_value%256
        
        G_value = 0
        for value in list(control_section):
            if value != ",":
                G_value += ord(value)
        G_value = G_value%256

        B_value = 0
        for condition in list(exchange_section):
            for value in list(condition):
                if value != ",":
                    B_value += ord(value)
        B_value = B_value%256

        return(str(R_value)+","+str(G_value)+","+str(B_value))

    def create_tiles(self):
        for x in range(self.map_size):
            for y in range(self.map_size):
                tile_at_xy = session.query(Tile).filter(Tile.x_coordinate == x).filter(Tile.y_coordinate == y).filter(Tile.simulation_relationship == Program.current_simulation).one()
                if tile_at_xy.tile_type == "Water":
                    self.tile_array[x][y] = Water_Tile(self.surface, self.simulation_surface, self.block_size, x*self.block_size, y*self.block_size, x, y, self.screen_width)
                elif tile_at_xy.tile_type == "Veg":
                    self.tile_array[x][y] = Veg_Tile(self.simulation_map, self.surface, self.simulation_surface, self.block_size, x*self.block_size, y*self.block_size, x, y, self.screen_width)
                elif tile_at_xy.tile_type == "Fruit":
                    self.tile_array[x][y] = Fruit_Tile(self.simulation_map, self.surface, self.simulation_surface, self.block_size, x*self.block_size, y*self.block_size, x, y, self.screen_width, True)
                elif tile_at_xy.tile_type == "Tree":
                    self.tile_array[x][y] = Fruit_Tile(self.simulation_map, self.surface, self.simulation_surface, self.block_size, x*self.block_size, y*self.block_size, x, y, self.screen_width, False)
                elif tile_at_xy.tile_type == "Meat":
                    self.tile_array[x][y] = Meat_Tile(self.simulation_map, self.surface, self.simulation_surface, self.block_size, x*self.block_size, y*self.block_size, x, y, self.screen_width)
                elif tile_at_xy.tile_type == "Organism":
                    self.tile_array[x][y] = Organism_Tile(self.simulation_map, self.surface, self.simulation_surface, self.block_size, x*self.block_size, y*self.block_size, x, y, self.screen_width, tile_at_xy)
                    self.organism_tiles.append(self.tile_array[x][y])
                else:
                    self.tile_array[x][y] = Simulation_Tile(self.surface, self.simulation_surface, self.block_size, x*self.block_size, y*self.block_size, x, y, self.screen_width)

    def find_tile_neighbours(self):
        for tile_row in self.tile_array:
            for tile in tile_row:
                if tile.x_coordinate > 0:
                    tile.neighbouring_tiles.append(self.tile_array[tile.x_coordinate-1][tile.y_coordinate])
                if tile.x_coordinate < self.map_size-1:
                    tile.neighbouring_tiles.append(self.tile_array[tile.x_coordinate+1][tile.y_coordinate])
                if tile.y_coordinate > 0:
                    tile.neighbouring_tiles.append(self.tile_array[tile.x_coordinate][tile.y_coordinate-1])
                if tile.y_coordinate < self.map_size-1:
                    tile.neighbouring_tiles.append(self.tile_array[tile.x_coordinate][tile.y_coordinate+1])

    def draw_tiles(self):
        for x in range(self.map_size):
            for y in range(self.map_size):
                self.tile_array[x][y].draw_tile()
                if self.tile_array[x][y].tile_type == "Organism":
                    self.tile_array[x][y].draw_organism()

    def draw_buttons(self):
        if self.simulation_state == 0:
            pygame.draw.rect(self.surface,BLACK,[self.pause_button_position[0],self.pause_button_position[1],140,40]) 
            pygame.draw.rect(self.surface,WHITE,[self.pause_button_position[0],self.pause_button_position[1],140,40],1) 
            self.surface.blit(self.start_text , (self.pause_button_position[0]+30,self.pause_button_position[1])) 
        elif self.simulation_state == 1:
            pygame.draw.rect(self.surface,BLACK,[self.pause_button_position[0],self.pause_button_position[1],140,40]) 
            pygame.draw.rect(self.surface,WHITE,[self.pause_button_position[0],self.pause_button_position[1],140,40],1) 
            self.surface.blit(self.pause_text , (self.pause_button_position[0]+30,self.pause_button_position[1])) 
        elif self.simulation_state == 2:
            pygame.draw.rect(self.surface,BLACK,[self.pause_button_position[0],self.pause_button_position[1],140,40]) 
            pygame.draw.rect(self.surface,WHITE,[self.pause_button_position[0],self.pause_button_position[1],140,40],1)
            self.surface.blit(self.play_text , (self.pause_button_position[0]+30,self.pause_button_position[1]))

        pygame.draw.rect(self.surface,WHITE,[self.save_button_position[0],self.save_button_position[1],140,40],1) 
        self.surface.blit(self.save_text , (self.save_button_position[0]+30,self.save_button_position[1])) 

        pygame.draw.rect(self.surface,WHITE,[self.quit_button_position[0],self.quit_button_position[1],140,40],1) 
        self.surface.blit(self.quit_text , (self.quit_button_position[0]+30,self.quit_button_position[1]))

        pygame.draw.rect(self.surface,WHITE,[self.analysis_button_position[0],self.analysis_button_position[1],180,40],1) 
        self.surface.blit(self.analysis_text , (self.analysis_button_position[0]+30,self.analysis_button_position[1]))

    def move_organisms(self):
        for organism_to_move in self.organisms:
            movement_direction = random.randint(0,4)
            if movement_direction == 0:
                movement_direction = self.move_up(organism_to_move)
            
            elif movement_direction == 1:
                movement_direction = self.move_right(organism_to_move)
            
            elif movement_direction == 2:
                movement_direction = self.move_down(organism_to_move)

            elif movement_direction == 3:
                movement_direction = self.move_left(organism_to_move)

            elif movement_direction == 4:
                pass

    def move_up(self, organism_to_move):
        if organism_to_move.y_position > 0:
            if self.tile_array[organism_to_move.x_position][organism_to_move.y_position-1].tile_type=="Blank":
                tile_to_move_from = organism_to_move.tile_relationship
                tile_to_move_to = session.query(Tile).filter(Tile.x_coordinate==organism_to_move.x_position).filter(Tile.y_coordinate==organism_to_move.y_position-1).filter(Tile.simulation_relationship==self.simulation).one()
                tile_to_move_from.tile_type = "Blank"
                tile_to_move_to.tile_type = "Organism"
                self.tile_array[organism_to_move.x_position][organism_to_move.y_position].tile_type="Blank"
                self.tile_array[organism_to_move.x_position][organism_to_move.y_position-1].tile_type="Organism"
                tile_to_move_from.organism_relationship = None
                tile_to_move_from.organism_id = None
                tile_to_move_to.organism_relationship = organism_to_move
                tile_to_move_to.organism_id = organism_to_move.id
                organism_to_move.y_position -= 1
                session.commit()
                return 0
            else:
                return 4
        else:
            return(4)

    def move_right(self, organism_to_move):
        if organism_to_move.x_position < self.map_size-1:
            if self.tile_array[organism_to_move.x_position+1][organism_to_move.y_position].tile_type=="Blank":
                tile_to_move_from = organism_to_move.tile_relationship
                tile_to_move_to = session.query(Tile).filter(Tile.x_coordinate==organism_to_move.x_position+1).filter(Tile.y_coordinate==organism_to_move.y_position).filter(Tile.simulation_relationship==self.simulation).one()
                tile_to_move_from.tile_type = "Blank"
                tile_to_move_to.tile_type = "Organism"
                self.tile_array[organism_to_move.x_position][organism_to_move.y_position].tile_type="Blank"
                self.tile_array[organism_to_move.x_position+1][organism_to_move.y_position].tile_type="Organism"
                tile_to_move_from.organism_relationship = None
                tile_to_move_from.organism_id = None
                tile_to_move_to.organism_relationship = organism_to_move
                tile_to_move_to.organism_id = organism_to_move.id
                organism_to_move.x_position += 1
                session.commit()
                return 1
            else:
                return 4
        else:
            return(4)

    def move_down(self, organism_to_move):
        if organism_to_move.y_position < self.map_size-1:
            if self.tile_array[organism_to_move.x_position][organism_to_move.y_position+1].tile_type=="Blank":
                tile_to_move_from = organism_to_move.tile_relationship
                tile_to_move_to = session.query(Tile).filter(Tile.x_coordinate==organism_to_move.x_position).filter(Tile.y_coordinate==organism_to_move.y_position+1).filter(Tile.simulation_relationship==self.simulation).one()
                tile_to_move_from.tile_type = "Blank"
                tile_to_move_to.tile_type = "Organism"
                self.tile_array[organism_to_move.x_position][organism_to_move.y_position].tile_type="Blank"
                self.tile_array[organism_to_move.x_position][organism_to_move.y_position+1].tile_type="Organism"
                tile_to_move_from.organism_relationship = None
                tile_to_move_from.organism_id = None
                tile_to_move_to.organism_relationship = organism_to_move
                tile_to_move_to.organism_id = organism_to_move.id
                organism_to_move.y_position += 1
                session.commit()
                return 2
            else:
                return 4
        else:
            return(4)

    def move_left(self, organism_to_move):
        if organism_to_move.x_position > 0:
            if self.tile_array[organism_to_move.x_position-1][organism_to_move.y_position].tile_type=="Blank":
                tile_to_move_from = organism_to_move.tile_relationship
                tile_to_move_to = session.query(Tile).filter(Tile.x_coordinate==organism_to_move.x_position-1).filter(Tile.y_coordinate==organism_to_move.y_position).filter(Tile.simulation_relationship==self.simulation).one()
                tile_to_move_from.tile_type = "Blank"
                tile_to_move_to.tile_type = "Organism"
                self.tile_array[organism_to_move.x_position][organism_to_move.y_position].tile_type="Blank"
                self.tile_array[organism_to_move.x_position-1][organism_to_move.y_position].tile_type="Organism"
                tile_to_move_from.organism_relationship = None
                tile_to_move_from.organism_id = None
                tile_to_move_to.organism_relationship = organism_to_move
                tile_to_move_to.organism_id = organism_to_move.id
                organism_to_move.x_position -= 1
                session.commit()
                return 3
            else:
                return 4
        else:
            return 4
   
    def check_area_around(self, tile):
        for neighbour in tile.neighbouring_tiles:
            action_performed = False
            if neighbour.tile_type == "Organism":
                if self.match(neighbour.organism_on_tile.reproduction_code, tile.organism_on_tile.reproduction_code):
                    action_performed = self.reproduce(tile.organism_on_tile, neighbour.organism_on_tile)
                else:
                    if self.hide(tile.organism_on_tile, neighbour.organism_on_tile):
                        action_performed=False
                    else:
                        self.attack(tile.organism_on_tile, neighbour.organism_on_tile)
                        action_performed = True
            elif neighbour.tile_type == "Meat" or neighbour.tile_type == "Veg" or neighbour.tile_type == "Fruit" and action_performed == False:
                self.eat_food(tile.organism_on_tile, neighbour.food_on_tile)
                action_performed = True
            elif neighbour.tile_type == "Water" and action_performed == False:
                self.drink_water(tile.organism_on_tile)
                action_performed = True

    def match(self, organism_1_code, organism_2_code):
        match = False
        total = 0
        for i in range(min(len(organism_1_code), len(organism_2_code))):
            if list(organism_1_code)[i]==list(organism_2_code)[i]:
                total+=1
        if total >= 0.75*min(len(organism_1_code), len(organism_2_code)):
            match = True
        return match

    def reproduce(self, organism_1, organism_2):
        commas_filtered_1 = list(filter(lambda a: a != ",", list(organism_1.chromosome)))
        organism_1_chromosome = list(filter(lambda a: a != "|", commas_filtered_1))
        commas_filtered_2 = list(filter(lambda a: a != ",", list(organism_2.chromosome)))
        organism_2_chromosome = list(filter(lambda a: a != "|", commas_filtered_2))
        if self.ready_to_reproduce(organism_1, organism_2, organism_1_chromosome, organism_2_chromosome):
            crossover_point = random.randint(1, min(len(organism_1.chromosome)-1, len(organism_2.chromosome)-1))
            if list(organism_1.chromosome)[crossover_point] == "|" or list(organism_1.chromosome)[crossover_point] == ",":
                new_organism_chromosome = organism_1.chromosome[0:crossover_point] + organism_2.chromosome[crossover_point:]
            else:
                new_organism_chromosome = organism_1.chromosome
            tag_section = new_organism_chromosome.split("|")[0]
            control_section = new_organism_chromosome.split("|")[1]
            exchange_section = new_organism_chromosome.split("|")[2]
            new_organism_chromosome = self.randomize_chromosome(tag_section, control_section, exchange_section)

            organism_placed = False
            for tile in self.tile_array[organism_1.x_position][organism_1.y_position].neighbouring_tiles:
                if tile.tile_type == "Blank" and organism_placed == False:
                    new_organism = Organism(chromosome=new_organism_chromosome, reservoir="abcd", colour=self.find_colour(tag_section, control_section, exchange_section), reproduction_code=control_section.split(",")[0], x_position=tile.x_coordinate, y_position=tile.y_coordinate, species_id=organism_1.species_id, species_relationship=organism_1.species_relationship, simulation_id=self.simulation.id, simulation_relationship=self.simulation)
                    session.add(new_organism)
                    tile_at_xy = session.query(Tile).filter(Tile.x_coordinate == tile.x_coordinate).filter(Tile.y_coordinate == tile.y_coordinate).filter(Tile.simulation_relationship == Program.current_simulation).one()
                    tile_at_xy.organism_id = new_organism.id
                    tile_at_xy.organism_relationship = new_organism
                    tile_at_xy.tile_type = "Organism"
                    session.commit()
                    organism_placed = True
                    self.organisms.append(new_organism)
                    self.tile_array[new_organism.x_position][new_organism.y_position].tile_type=Organism_Tile(self.simulation_map, self.surface, self.simulation_surface, self.block_size, new_organism.x_position*self.block_size, new_organism.y_position*self.block_size, new_organism.x_position, new_organism.y_position, self.screen_width, tile_at_xy)
            if organism_placed == False:
                pass
                print("Replace Organism 1")                
            return True
        else:
            return False

    def ready_to_reproduce(self, organism_1, organism_2, chromosome_value_1, chromosome_value_2):
        #has_resources = True
        #reservoir_copy_1 = list(organism_1.reservoir)
        #reservoir_copy_2 = list(organism_2.reservoir)
        #print(organism_1)
        #print(organism_2)
        #for character in chromosome_value_1[:int(len(chromosome_value_1))]:
        #    try:
        #        reservoir_copy_1.remove(character)
        #    except:
        #        has_resources = False
        #for character in chromosome_value_2[int(len(chromosome_value_1)):]:
        #    try:
        #        reservoir_copy_2.remove(character)
        #    except:
        #        has_resources = False
        #print(has_resources)
        #return has_resources
        return True

    def hide(self, organism_1, organism_2):
        hide = False
        attack_tag = list(organism_1.chromosome.split("|")[0].split(",")[0])
        hide_tag = list(organism_2.chromosome.split("|")[1].split(",")[0])
        if len(hide_tag) < len(attack_tag):
            for i in range(len(hide_tag)):
                if hide_tag[i] != attack_tag[i] and hide_tag[i] != "#":
                    hide = True
        else:
            hide = True
        return(hide)

    def attack(self, organism_1, organism_2):
        value = 0
        attack_tag_elements = list(organism_1.chromosome.split("|")[0].split(",")[0])
        defence_tag_elements = list(organism_2.chromosome.split("|")[0].split(",")[1])
        for i in range(max(len(attack_tag_elements), len(defence_tag_elements))):
            if i <= len(attack_tag_elements)-1:
                if i > len(defence_tag_elements)-1:
                    value += 1
                elif attack_tag_elements[i] == defence_tag_elements[i]:
                    value += 2
                elif attack_tag_elements[i] == "#":
                    value += 1
                else:
                    value -= 1
        if value > 0:
            resources_given = organism_2.reservoir[0:value]
            organism_2.reservoir = organism_2.reservoir[value:]
            organism_1.reservoir += resources_given
            session.commit()
            if len(organism_2.reservoir) == 0:
                self.convert_to_meat(organism_2)

    def convert_to_meat(self, organism_to_convert):
        nutritional_value=""
        for letter in list(organism_to_convert.chromosome):
            if letter != "," and letter != "|":
                nutritional_value += letter
        new_food = Food(food_type="Meat", nutritional_value=nutritional_value, consumption_code="cdccdddccd", x_coordinate=organism_to_convert.x_position, y_coordinate=organism_to_convert.y_position, map_id=self.simulation_map.id, map_relationship=self.simulation_map, tile_relationship=organism_to_convert.tile_relationship)
        
        tile = organism_to_convert.tile_relationship
        organism_to_convert.tile_relationship.tile_type = "Meat"
        tile.organism_relationship = None
        tile.organism_id = None
        tile.food_relationship = new_food
        tile.food_id = new_food.id
        session.add(new_food)
        session.commit()

        self.tile_array[organism_to_convert.x_position][organism_to_convert.y_position].tile_type = Meat_Tile(self.simulation_map, self.surface, self.simulation_surface, self.block_size, organism_to_convert.x_position*self.block_size, organism_to_convert.y_position*self.block_size, organism_to_convert.x_position, organism_to_convert.y_position, self.screen_width)

        organism_to_convert.species_relationship = None
        organism_to_convert.species_id = None
        organism_to_convert.simulation_relationship = None
        organism_to_convert.simulation_id = None
        self.organisms.remove(organism_to_convert)
        
        session.delete(organism_to_convert)
        session.commit()

    def eat_food(self, organism, food):
        food_consumption_code = list(food.consumption_code)
        organism_consumer_code = list(organism.chromosome.split("|")[1].split(",")[2])
        total = 0
        if food.food_type == "Meat":
            for i in range(len(organism_consumer_code)):
                if i<len(food_consumption_code)-1:
                    if organism_consumer_code[i]==food_consumption_code[i]:
                            total+=2
                    if organism_consumer_code[i]=="#":
                        total+=1
            if total > 0:
                organism.reservoir += food.nutritional_value[0:total]
                food.nutritional_value = food.nutritional_value[total:]
                if len(food.nutritional_value)==0:
                    food.food_type = "Deleted"
                    food.tile_relationship.tile_type = "Blank"
                    food.tile_relationship.tile_id = None
                    food.tile_relationship.food_relationship = None
                    session.delete(food)
                session.commit()
        elif food.food_type == "Fruit":
            for i in range(len(organism_consumer_code)):
                if i<len(food_consumption_code)-1:
                    if organism_consumer_code[i]==food_consumption_code[i]:
                        total+=2
                    if organism_consumer_code[i]=="#":
                        total+=1
            if total > 0:            
                organism.reservoir += food.nutritional_value[0:total]
                food.nutritional_value = food.nutritional_value[total:]
                session.commit()
            if len(food.nutritional_value)==0:
                food.tile_relationship.tile_type = "Tree"
                food.food_type = "Tree"
                session.commit()

        elif food.food_type == "Veg":
            for i in range(len(organism_consumer_code)):
                if i<len(food_consumption_code)-1:
                    if organism_consumer_code[i]==food_consumption_code[i]:
                        total+=2
                    if organism_consumer_code[i]=="#":
                        total+=1
            if total > 0:            
                organism.reservoir += food.nutritional_value[0:total]
                session.commit()

    def drink_water(self, organism):
        organism.reservoir += "aa"
        session.commit()

    def start(self):
        self.simulation_state = 1
        self.draw_buttons()
        self.organisms = session.query(Organism).filter(Organism.simulation_id==self.simulation.id).all()

    def pause(self):
        self.simulation_state = 2
        self.draw_buttons()

    def play(self):
        self.simulation_state = 1
        self.draw_buttons()

    def save(self):
        print("Save")

    def quit_simulation(self):
        Program.current_simulation = None
        Home_screen()

    def analysis(self):
        print("Analysis")

class Simulation_Tile():
    def __init__(self, surface, simulation_surface, block_size, x_position, y_position, x_coordinate, y_coordinate, screen_width):
        self.surface = surface
        self.simulation_surface = simulation_surface
        self.block_size = block_size
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.x_position = x_position
        self.y_position = y_position
        self.screen_width = screen_width
        self.image = "Grass.png"
        self.tile_type = "Blank"
        self.neighbouring_tiles = []

    def draw_tile(self):
        image_to_draw = pygame.image.load(self.image).convert_alpha()
        scaled_image = pygame.transform.scale(image_to_draw, (self.block_size, self.block_size))
        self.simulation_surface.blit(scaled_image, pygame.Rect(self.x_position, self.y_position, self.block_size, self.block_size).topleft)
        self.surface.blit(self.simulation_surface, (int(self.screen_width*(1/4)),50))

class Water_Tile(Simulation_Tile):
    def __init__(self, surface, simulation_surface, block_size, x_position, y_position, x_coordinate, y_coordinate, screen_width):
        super().__init__(surface, simulation_surface, block_size, x_position, y_position, x_coordinate, y_coordinate, screen_width)
        self.image = "Water_on_grass.png"
        self.tile_type = "Water"

class Veg_Tile(Simulation_Tile):
    def __init__(self, food_map, surface, simulation_surface, block_size, x_position, y_position, x_coordinate, y_coordinate, screen_width):
        super().__init__(surface, simulation_surface, block_size, x_position, y_position, x_coordinate, y_coordinate, screen_width)
        self.food_on_tile = session.query(Food).filter(Food.x_coordinate==x_coordinate).filter(Food.y_coordinate==y_coordinate).filter(Food.map_id==food_map.id).one()
        self.image = "Grass_on_grass.png"
        self.tile_type = "Veg"

class Fruit_Tile(Simulation_Tile):
    def __init__(self, food_map, surface, simulation_surface, block_size, x_position, y_position, x_coordinate, y_coordinate, screen_width, fruit_on_tree):
        super().__init__(surface, simulation_surface, block_size, x_position, y_position, x_coordinate, y_coordinate, screen_width)
        self.food_on_tile = session.query(Food).filter(Food.x_coordinate==x_coordinate).filter(Food.y_coordinate==y_coordinate).filter(Food.map_id==food_map.id).one()
        if fruit_on_tree:
            self.image = "Fruit_on_grass_with_fruit.png"
        else:
            self.image = "Fruit_on_grass.png"
        self.tile_type = "Fruit"

class Meat_Tile(Simulation_Tile):
    def __init__(self, food_map, surface, simulation_surface, block_size, x_position, y_position, x_coordinate, y_coordinate, screen_width):
        super().__init__(surface, simulation_surface, block_size, x_position, y_position, x_coordinate, y_coordinate, screen_width)  
        self.food_on_tile = session.query(Food).filter(Food.x_coordinate==x_coordinate).filter(Food.y_coordinate==y_coordinate).filter(Food.map_id==food_map.id).one()
        self.image = "Meat_on_grass.png"
        self.tile_type = "Meat"

class Organism_Tile(Simulation_Tile):
    def __init__(self, simulation, surface, simulation_surface, block_size, x_position, y_position, x_coordinate, y_coordinate, screen_width, tile_at_xy):
        super().__init__(surface, simulation_surface, block_size, x_position, y_position, x_coordinate, y_coordinate, screen_width)
        self.organism_on_tile = tile_at_xy.organism_relationship
        r, g, b = self.organism_on_tile.colour.strip().split(",")
        self.block_size = block_size
        self.colour_tuple = (int(r),int(g),int(b))
        self.simulation_surface = simulation_surface
        self.x_position = x_position
        self.y_position = y_position
        self.tile_type = "Organism"
        self.block_size = block_size
    def draw_organism(self):
        pygame.draw.circle(self.simulation_surface, self.colour_tuple, (int(self.x_position+(self.block_size/2)),int(self.y_position+(self.block_size/2))), int(self.block_size/7))
        pygame.draw.circle(self.simulation_surface, (0,0,0), (int(self.x_position+(self.block_size/2)),int(self.y_position+(self.block_size/2))), int(self.block_size/7), 1)

Program()