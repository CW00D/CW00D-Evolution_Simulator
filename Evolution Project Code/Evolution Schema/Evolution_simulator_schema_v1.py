import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

Base = declarative_base()

engine = create_engine('sqlite:///evolution_simulator.db', echo=True)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    username = Column(String(20))
    password = Column(String(20))

    simulations_realtionship = relationship("Simulation", back_populates='user_relationship')

    def __repr__(self):
        return "<User(id: {0}, name: {1}, username: {2}, password: {3})".format(self.id, self.name, self.username, self.password)   

class Simulations(Base):
    __tablename__ = "simulations"
    id = Column(Integer, primary_key=True)
    current_turn = Column(Integer)
    length_of_turn = Column(Integer)
    number_of_starting_organisms = Column(Integer)
    number_of_starting_species = Column(Integer)
    current_number_of_organisms = Column(Integer)
    current_number_of_species = Column(Integer)

    user_id = Column(ForeignKey("users.id"))
    user_relationship = relationship("User", back_populates='simulations_relationship')

    species_relaionship = relationship("Species", back_populates='simulation_relationship')

    map_relationship = relationship("Map", back_populates='simulation_realationship')

    def __repr__(self):
        return "<Simulation(id: {0}, current turn: {1}, length of turn: {2}, current organisms: {3}, current species: {4}, user: {5})>".format(self.id, self.current_turn, self.length_of_turn, self.current_number_of_organisms, self.current_number_of_species, self.user_id)

class Species(Base):
    __tablename__ = "species"
    id = Column(Integer, primary_key=True)
    reproduction_code = Column(String(50))
    species_colour = Column(String(10))

    simulation_id = Column(ForeignKey("simulations.id"))
    simulation_relationship = relationship("Simulation", back_populates='species_relationship')

    species_history_relaionship = relationship("SpeciesHistory", back_populates='species_relationship')

    organism_relationship = relationship("Organism", back_populates='species_relationship')

    def __repr__(self):
        return "<Species(species id: {0}, reproduction code: {1}, scpecies colour: {2}, simulation: {3})>".format(self.id, self.reproduction_code, self.species_colour, self.simulation_id)

class SpeciesHistory(Base):
    __tablename__ = "species_history"
    id = Column(Integer, primary_key=True)
    population = Column(Integer)
    average_size = Column(Integer)
    average_speed = Column(Integer)

    species_id = Column(ForeignKey("species.id"))
    species_relationship = relationship("Species", back_populates='species_history_relationship')

    def __repr__(self):
        return "<SpeciesHistory(species history turn: {0}, population: {1}, average size: {2}, average speed: {3}, species: {4})>".format(self.id, self.population, self.average_size, self.average_speed, self.species_id)

class Organism(Base):
    __tablename__ = "organisms"
    id = Column(Integer, primary_key=True)
    food_required = Column(Integer)
    current_food = Column(Integer)
    water_required = Column(Integer)
    current_water = Column(Integer)
    fat_content = Column(Integer)
    reproduction_code = Column(Integer)
    size = Column(Integer)
    x_position = Column(Integer)
    y_position = Column(Integer)
    range_of_detection = Column(Integer)
    speed = Column(Integer)

    species_id = Column(ForeignKey("species.id"))
    species_relationship = relationship("Species", back_populates='organism_relationship')

    food_relationship = relationship("Food", back_populates='organism_relationship')

    def __repr__(self):
        return "<Organism(organism id: {0}, speces{1}, food: {2}/{3}, water: {4}/{5}, fat content: {6}, reproduction code: {7}, size: {8}, position: ({9}:{10}), range_of_detection: {11}, speed: {12})>".format(self.id, self.species_id, self.current_food, self.food_required, self.current_water, self.water_required, self.fat_content, self.reproduction_code, self.size, self.x_position, self.y_position, self.range_of_detection, self.speed)

class Map(Base):
    __tablename__ = "maps"
    id = Column(Integer, primary_key=True)
    map_size = Column(Integer)
    number_of_food_sources = Column(Integer)
    number_of_water_sources = Column(Integer)
    average_temperature = Column(Integer)
    temperature_range = Column(Integer) 

    simulation_id = Column(ForeignKey("simulations.id"))
    simulation_relationship = relationship("Simulation", back_populates='map_relationship')

    food_relationship = relationship("Food", back_populates="map_relationship")

    def __repr__(self):
        return "<Map(map_id: {0}, map size: {1}, number of food sources: {2}, number of water sources: {3}, averatge temperature: {4}, temperature range: {5}, simulation id: {6})>".format(self.id, self.map_size, self.number_of_food_sources, self.number_of_water_sources, self.average_temperature, self.temperature_range, self.simulation_id)

class Food(Base):
    __tablename__ = "foods"
    id = Column(Integer, primary_key=True)
    food_type = Column(Integer)
    nutritional_value = Column(Integer)
    position_x = Column(Integer)
    position_y = Column(Integer) 

    map_id = Column(ForeignKey("simulations.id"))
    map_relationship = relationship("Map", back_populates='food_realtionship')

    organism_id = Column(ForeignKey("organisms.id"))
    organism_relationship = relationship("Organism", back_populates='food_relationship')

    def __repr__(self):
        return "<Food(food id: {0}, nutritional value: {1}, position: ({2},{3}), map id: {4}, organism id: {5})>".format(self.id, self.food_type, self.nutritional_value, self.position_x, self.position_y, self.map_id, self.organism_id)

session.commit()