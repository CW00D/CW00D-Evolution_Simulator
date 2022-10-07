import random

class Organism:
    def __init__(self, chromosome, reservoir):
        #chromosome_structure = AttackTag,DefenceTag,ExchangeCondition
        self.chromosome = chromosome
        chromosome_components = chromosome.split("|")
        self.attack_tag = chromosome_components[0].split(",")[0]
        self.defence_tag = chromosome_components[0].split(",")[1]
        self.exchange_condition = chromosome_components[1]
        self.transform_conditions = chromosome_components[2].split(",")  
        self.reservoir = reservoir
        self.dead = False
    
    def attack(self, organism_to_attack):
        total = 0
        attack_tag_elements = list(self.attack_tag)
        defence_tag_elements = list(organism_to_attack.defence_tag)
        for i in range(max(len(attack_tag_elements), len(defence_tag_elements))):
            if i <= len(attack_tag_elements)-1:
                if i > len(defence_tag_elements)-1:
                    total += 1
                elif attack_tag_elements[i] == defence_tag_elements[i]:
                    total += 2
        return total        

    def give_resources(self, organism_to_give_to, number_of_resources_to_give):
        resources = self.reservoir
        if number_of_resources_to_give <= len(resources):
            resources_to_give = []
            for i in range(number_of_resources_to_give):
                resources_to_give.append(self.reservoir.pop(-1))
        else:
            resources_to_give = resources
            self.dead = True
        return(resources_to_give)

    def add_resources(self, resources_given):
        for i in resources_given:
            self.reservoir.append(i)

    def exchange(self, organism_to_exchange_with):
        exchange_possible = True
        exchange_values = list(self.exchange_condition)
        attack_values = list(organism_to_exchange_with.attack_tag)
        if len(exchange_values) < len(attack_values):
            for i in range(len(exchange_values)):
                if exchange_values[i] != attack_values[i] and exchange_values[i] != "#":
                    exchange_possible = False
        else:
            exchange_possible = False
        return(exchange_possible)

    def transform(self):
        reservoir_copy = self.reservoir.copy()
        transformation_possible = True
        for transform in self.transform_conditions:
            resource_to_transform_from = transform[0]
            resource_to_transform_to = transform[1]
            resource_transformation_cost = list(transform[2:])
            
            if resource_to_transform_from in reservoir_copy:
                index = reservoir_copy.index(resource_to_transform_from)
                del reservoir_copy[index]
            else:
                transformation_possible = False
            
            for resource in resource_transformation_cost:
                if resource in reservoir_copy:
                    index = reservoir_copy.index(resource)
                    del reservoir_copy[index]
                else:
                    transformation_possible = False
            
            if transformation_possible:        
                reservoir_copy.append(resource_to_transform_to)
                self.reservoir = reservoir_copy    


organism_1 = Organism("abbaca,aabab|b##db|abccc", ["a", "b", "c", "a", "a", "b","a", "a", "d"])
organism_2 = Organism("bbadbc,abaa|a|TransformCondition", ["a", "b", "c", "a", "a", "b","a", "a", "d"])

def fight(organism_1, organism_2):
    exchange_1 = organism_1.exchange(organism_2)
    exchange_2 = organism_2.exchange(organism_1)

    if exchange_1 and exchange_2:
        pass
    elif exchange_1:
        if random.randint(0,1)<0.5:
            value = organism_1.attack(organism_2) - organism_2.attack(organism_1)
            if value > 0:
                resources_given = organism_2.give_resources(organism_1, value)
                organism_1.add_resources(resources_given)
            elif value < 0:
                resources_given = organism_1.give_resources(organism_2, abs(value))
                organism_2.add_resources(resources_given)
    elif exchange_2:
        if random.randint(0,1)<0.25:
            value = organism_1.attack(organism_2) - organism_2.attack(organism_1)
            if value > 0:
                resources_given = organism_2.give_resources(organism_1, value)
                organism_1.add_resources(resources_given)
            elif value < 0:
                resources_given = organism_1.give_resources(organism_2, abs(value))
                organism_2.add_resources(resources_given)
    else:
        value = organism_1.attack(organism_2) - organism_2.attack(organism_1)
        if value > 0:
            resources_given = organism_2.give_resources(organism_1, value)
            organism_1.add_resources(resources_given)
        elif value < 0:
            resources_given = organism_1.give_resources(organism_2, abs(value))
            organism_2.add_resources(resources_given)
    return(organism_1,organism_2)

organism_1, organism_2 = fight(organism_1, organism_2)

organism_1.transform()