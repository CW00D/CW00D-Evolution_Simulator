import random

class Organism:
    def __init__(self, chromosome, reservoir):
        #chromosome_structure = AttackTag,DefenceTag,ExchangeCondition
        self.chromosome = chromosome
        self.attack_tag = chromosome.split(",")[0]
        self.defence_tag = chromosome.split(",")[1]
        self.exchange_condition = chromosome.split(",")[2]
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

organism_1 = Organism("abbaca,aabab,b##db", ["a", "b", "c", "a", "a", "b","a", "a", "d"])
organism_2 = Organism("bbadbc,abaa,a", ["a", "b", "c", "a", "a", "b","a", "a", "d"])

def fight(organism_1, organism_2):
    exchange_1 = organism_1.exchange(organism_2)
    exchange_2 = organism_2.exchange(organism_1)

    if exchange_1 and exchange_2:
        print("Run")
        pass
    elif exchange_1:
        print("Chance_1")
        if random.randint(0,1)<0.5:
            value = organism_1.attack(organism_2) - organism_2.attack(organism_1)
            if value > 0:
                resources_given = organism_2.give_resources(organism_1, value)
                organism_1.add_resources(resources_given)
            elif value < 0:
                resources_given = organism_1.give_resources(organism_2, abs(value))
                organism_2.add_resources(resources_given)
    elif exchange_2:
        print("Chance_2")
        if random.randint(0,1)<0.25:
            value = organism_1.attack(organism_2) - organism_2.attack(organism_1)
            if value > 0:
                resources_given = organism_2.give_resources(organism_1, value)
                organism_1.add_resources(resources_given)
            elif value < 0:
                resources_given = organism_1.give_resources(organism_2, abs(value))
                organism_2.add_resources(resources_given)
    else:
        print("fight")
        value = organism_1.attack(organism_2) - organism_2.attack(organism_1)
        if value > 0:
            resources_given = organism_2.give_resources(organism_1, value)
            organism_1.add_resources(resources_given)
        elif value < 0:
            resources_given = organism_1.give_resources(organism_2, abs(value))
            organism_2.add_resources(resources_given)
    return(organism_1,organism_2)

organism_1, organism_2 = fight(organism_1, organism_2)
print(organism_1.reservoir)
print(organism_2.reservoir)
