class Organism:
    def __init__(self, chromosome, reservoir):
        self.chromosome = chromosome
        self.attack_tag = chromosome.split(",")[0]
        self.defence_tag = chromosome.split(",")[1]
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

organism_1 = Organism("abbaca,aabab", ["a", "b", "c", "a", "a", "b","a", "a", "d"])
organism_2 = Organism("bbadbc,dabaa", ["a", "b", "c", "a", "a", "b","a", "a", "d"])

value = organism_1.attack(organism_2) - organism_2.attack(organism_1)
if value > 0:
    resources_given = organism_2.give_resources(organism_1, value)
    organism_1.add_resources(resources_given)
elif value < 0:
    resources_given = organism_1.give_resources(organism_2, abs(value))
    organism_2.add_resources(resources_given)

print(organism_1.reservoir)
print(organism_2.reservoir)

reproduce(organism_1, organism_2)