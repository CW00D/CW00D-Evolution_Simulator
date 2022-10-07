from Evolution_simulator_schema_v2 import User, Simulation, Species, SpeciesHistory, Organism, Map, Food
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///evolution_simulator.db', echo=False)
session = sessionmaker(bind=engine)()


#____USER____

    #user = session.query(User).first()
    #print(user)

    #user = session.query(User).order_by(User.id.desc()).first()
    #print(user)

    #user = session.query(User).filter(User.name == "Rosamond").one()
    #print(user)

    #user = session.query(User).filter(User.username == "rzumfelde1").one()
    #print(user)

    #user = session.query(User).filter(User.password == "RdVvqyy").one()
    #print(user)

    #simulations = session.query(Simulation).filter(Simulation.user_relationship == user).all()
    #print(simulations)

    #user = session.query(User).first()
    #simulations = session.query(Simulation).filter(Simulation.user_relationship == user).all()
    #print(simulations)

    #user = session.query(User).first()
    #simulation = user.simulations_relationship
    #print(simulation)


#____SIMULATION____

    #simulation = session.query(Simulation).first()
    #print(simulation)

    #simulation = session.query(Simulation).order_by(Simulation.id.desc()).first()
    #print(simulation)

    #simulation = session.query(Simulation).filter(Simulation.current_turn == 54).first()
    #print(simulation)

    #simulation = session.query(Simulation).filter(Simulation.length_of_turn == 49).first()
    #print(simulation)

    #simulation = session.query(Simulation).filter(Simulation.starting_number_of_organisms == 58).first()
    #print(simulation)

    #simulation = session.query(Simulation).filter(Simulation.starting_number_of_species == 95).first()
    #print(simulation)

    #simulation = session.query(Simulation).filter(Simulation.current_number_of_organisms == 8).first()
    #print(simulation)

    #simulation = session.query(Simulation).filter(Simulation.current_number_of_species == 67).first()
    #print(simulation)

    #simulation = session.query(Simulation).first()
    #species = session.query(Species).filter(Species.simulation_relationship == simulation).all()
    #print(species)    

    #species = simulation.species_relationship
    #print(species)


    #simulation = session.query(Simulation).first()
    #test_map = session.query(Map).filter(Map.simulation_relationship == simulation).one()
    #print(test_map)  

    #simulation = session.query(Simulation).first()
    #map_test = simulation.map_relationship
    #print(map_test)

#____SPECIES____

    #species = session.query(Species).first()
    #print(species)

    #species = session.query(Species).order_by(Species.id.desc()).first()
    #print(species)

    #species = session.query(Species).filter(Species.reproduction_code == 3).first()
    #print(species)

    #species = session.query(Species).filter(Species.species_colour == 13).first()
    #print(species)

    #species = session.query(Species).first()
    #species_history = session.query(SpeciesHistory).filter(SpeciesHistory.species_relationship == species).all()
    #print(species_history)  

    #species = session.query(Species).first()
    #species_history = species.species_history_relationship
    #print(species_history)

    #species = session.query(Species).first()
    #organism = session.query(Organism).filter(Organism.species_relationship == species).all()
    #print(organism)    

    #species = session.query(Species).first()
    #organism = species.organism_relationship
    #print(organism)

#____SPECIESHISTORY____

    #species_history = session.query(SpeciesHistory).first()
    #print(species_history)

    #species_history = session.query(SpeciesHistory).order_by(SpeciesHistory.id.desc()).first()
    #print(species_history)

#species_history = session.query(SpeciesHistory).filter(SpeciesHistory.population == 74).first()
#print(species_history )

#species_history  = session.query(SpeciesHistory).filter(SpeciesHistory.average_size == 25).first()
#print(species_history)

#species_history  = session.query(SpeciesHistory).filter(SpeciesHistory.average_speed == 52).first()
#print(species_history)


#_____ORGANISMS____

    #organism= session.query(Organism).first()
    #print(organism)

    #organism = session.query(Organism).order_by(Organism.id.desc()).first()
    #print(organism)

    #organism = session.query(Organism).filter(Organism.current_food == 14).first()
    #print(organism)

    #organism = session.query(Organism).filter(Organism.food_required == 88).first()
    #print(organism)

    #organism = session.query(Organism).filter(Organism.current_water == 13).first()
    #print(organism)

    #organism = session.query(Organism).filter(Organism.water_required == 93).first()
    #print(organism)

    #organism = session.query(Organism).filter(Organism.fat_content == 32).first()
    #print(organism)

    #organism = session.query(Organism).filter(Organism.reproduction_code == 1).first()
    #print(organism)

    #organism = session.query(Organism).filter(Organism.size == 19).first()
    #print(organism)

    #organism = session.query(Organism).filter(Organism.x_position == 44).first()
    #print(organism)

    #organism = session.query(Organism).filter(Organism.y_position == 18).first()
    #print(organism)

    #organism = session.query(Organism).filter(Organism.range_of_detection == 3).first()
    #print(organism)

    #organism = session.query(Organism).filter(Organism.speed == 7).first()
    #print(organism)

    #organism = session.query(Organism).first()
    #food = session.query(Food).filter(Food.organism_relationship == organism).all()
    #print(food)    

    #organism = session.query(Organism).first()
    #food = organism.food_relationship
    #print(food)
 
 #____MAPS____

    #map_test = session.query(Map).first()
    #print(map_test)

    #map_test = session.query(Map).order_by(Map.id.desc()).first()
    #print(map_test)

    #map_test = session.query(Map).filter(Map.map_size == 60).first()
    #print(map_test)

    #map_test = session.query(Map).filter(Map.number_of_food_sources == 9).first()
    #print(map_test)

    #map_test = session.query(Map).filter(Map.number_of_water_sources == 16).first()
    #print(map_test)

    #map_test = session.query(Map).filter(Map.average_temperature == 32).first()
    #print(map_test)

    #map_test = session.query(Map).filter(Map.temperature_range == 5).first()
    #print(map_test)

    #map_test = session.query(Map).first()
    #food = session.query(Food).filter(Food.map_relationship == map_test).all()
    #print(food)    

    #map_test = session.query(Map).first()
    #food = map_test.food_relationship
    #print(food)

#____FOOD____

    #food = session.query(Food).first()
    #print(food)

    #food = session.query(Food).order_by(Food.id.desc()).first()
    #print(food)

    #food = session.query(Food).filter(Food.food_type == "veg").first()
    #print(food)

    #food = session.query(Food).filter(Food.nutritional_value == 60).first()
    #print(food)

    #food = session.query(Food).filter(Food.position_x == 16).first()
    #print(food)

    #food = session.query(Food).filter(Food.position_y == 98).first()
    #print(food)