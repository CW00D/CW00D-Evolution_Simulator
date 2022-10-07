import random
import re

class Organism:
    def __init__(self, chromosome, reservoir):
        #chromosome_structure = AttackTag,DefenceTag,ExchangeCondition
        self.chromosome = chromosome
        chromosome_components = chromosome.split("|")
        self.attack_and_deffence_tags = chromosome_components[0]
        self.attack_tag = chromosome_components[0].split(",")[0]
        self.defence_tag = chromosome_components[0].split(",")[1]
        self.exchange_condition = chromosome_components[1]
        self.transform_conditions = chromosome_components[2].split(",")  
        self.reservoir = reservoir
        self.dead = False
        self.colour = self.find_colour()
    
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

    def find_colour(self):
        R_value = 0
        for value in list(self.attack_and_deffence_tags):
            if value != ",":
                R_value += ord(value)
        R_value = R_value%256
        
        G_value = 0
        for value in list(self.exchange_condition):
            if value != ",":
                G_value += ord(value)
        G_value = G_value%256

        B_value = 0
        print(self.transform_conditions)
        for condition in list(self.transform_conditions):
            for value in list(condition):
                if value != ",":
                    B_value += ord(value)
        B_value = G_value%256

        return((R_value,G_value,B_value))

organism_1 = Organism("abbaca,aabab|b##db|abccc", ["a", "b", "c", "a", "a", "b","a", "a", "d"])
organism_2 = Organism("bbadbc,abaa|a|ac,ac", ["a", "b", "c", "a", "a", "b","a", "a", "d"])

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

def reproduce(organism_1, organism_2):
    print(organism_1, organism_2)

organism_1, organism_2 = fight(organism_1, organism_2)
print(organism_1.reservoir)
print(organism_2.reservoir)

organism_1.transform()
organism_2.transform()

reproduce(organism_1, organism_2)

#print("a" + "b"*random.randint(1,3) + "d"*random.randint(0,2))

print(organism_1.colour)
print(organism_2.colour)

string = "Hello"
print(string[0:1])
print(len(string[5:]))

test_list = [organism_1, organism_2]
print(test_list)
test_list.remove(organism_2)
print(test_list.index(organism_1))

organism_3 = Organism("abbaca,aabab|b##db|abccc", ["a", "b", "b", "a", "c", "a", "a", "a", "b", "a", "b", "b", "#", "#", "d", "b", "a", "b", "c", "c", "c"])

has_resources = True
commas_filtered = list(filter(lambda a: a != ",", list(organism_3.chromosome)))
pipes_filtered = list(filter(lambda a: a != "|", commas_filtered))
reservoir_copy = list(organism_3.reservoir)
for character in list(pipes_filtered):
    try:
        reservoir_copy.remove(character)
    except:
        has_resources = False
print(has_resources)
    
#return(all(elem in list(organism.reservoir) for elem in pipes_filtered))

text = "helol,lakd|ahdh"
print(re.split("[,/] ", text))

text = "python is, an easy;language; to, learn."
print(re.split("[;,] ", text))

print("hello".split(","))

text_1 = "hello"
text_2 = "hello"
index = 1
print(text_1[0:index]+text_2[index:])

chromosome_1 = "aa,aa|aa,aa,aa|aa,aa"
chromosome_2 = "bb,bb|bb,bb,bb|bb,bb"
chromosome_1 = chromosome_1.split("|")
chromosome_2 = chromosome_2.split("|")
print(chromosome_1)
print(chromosome_2)

print(3%2)
print(3%3)

text = "h"
print(text[2:])

print("hello".split(","))

print(type(1)== int)
print(type(0)== int)

try:
    int("a")
except:
    print("not int")

try:
    int("2")
except:
    print("not int")

print(2**2)

print(len(""))

for i in range(10):
    print(["a","b","c","d"][random.randint(0,3)])

print("hello".split("o")[1])

print("hello"[2])

for i in range(10):
    if i==5:
        break
    print(i)

print("".join("h,e,l,l,o".split(",")[2:]))

chromosome_1 = "aaa,aaa|aaa,aaa,aaaaaaa|aaaaa,aaaaa"
chromosome_2 = "bbbbbb,bbb|bbbbb,bbb,bbb|bbbbb,bbbbb"
chromosome_1_pipes = chromosome_1.split("|")
chromosome_2_pipes = chromosome_2.split("|")

crossover_point = random.randint(0,4)
print(crossover_point)
if crossover_point ==  1 or crossover_point == 4:
    if crossover_point == 1:
        new_chromosome = chromosome_1_pipes[0]+"|"+chromosome_2_pipes[1]+"|"+chromosome_2_pipes[2]
    elif crossover_point == 4:
        new_chromosome = chromosome_1_pipes[0]+"|"+chromosome_1_pipes[1]+"|"+chromosome_2_pipes[2]

elif crossover_point == 0 or crossover_point == 2 or crossover_point == 3:
    if crossover_point == 0:
        new_chromosome = chromosome_1_pipes[0].split(",")[0]+","+chromosome_2_pipes[0].split(",")[1]+"|"+chromosome_2_pipes[1]+"|"+chromosome_2_pipes[2]
    elif crossover_point == 2:
        new_chromosome = chromosome_1_pipes[0]+"|"+chromosome_1_pipes[1].split(",")[0]+","+chromosome_2_pipes[1].split(",")[1]+","+chromosome_2_pipes[1].split(",")[2]+"|"+chromosome_2_pipes[2]
    elif crossover_point == 3:
        new_chromosome = chromosome_1_pipes[0]+"|"+chromosome_1_pipes[1].split(",")[0]+","+chromosome_1_pipes[1].split(",")[1]+","+chromosome_2_pipes[1].split(",")[2]+"|"+chromosome_2_pipes[2]
print(new_chromosome)

print(list(range(0, 6)))
print([1]*3)
