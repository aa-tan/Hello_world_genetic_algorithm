import string
import random
from collections import Counter

population_size = 10
test_lengt = 50
target = "Hello world"


class Individual:
    ind_count = 0

    def __init__(self, case=None):
        if case is None:
            self.case = random_string()
        else:
            self.case = case
        self.score = calculate_fitness(self.case, target)
        Individual.ind_count += 1

    def __str__(self):
        return "Case: {}\nScore: {}".format(self.case, self.score)


def random_string(length=11, characters=string.ascii_letters+" "):
    return ''.join(random.choice(characters) for _ in range(length))


class Generation:
    gen_count = 0

    def __init__(self, individuals=None):
        if individuals is None:
            self.individuals = []
            for x in range(population_size):
                self.individuals.append(Individual())
        else:
            self.individuals = individuals
        Generation.gen_count += 1

    def __str__(self):
        fittest = select_fittest(self)
        return "Case: {}\nScore: {}\n".format(fittest.case, fittest.score)

    def get_all_individuals(self):
        ret = ""
        for item in self.individuals:
            ret += "{}\n".format(item)
        return ret


def individual_mutate(fittest):
    extracted = get_match(fittest)
    base = create_base(extracted)
    mutation = insert_random(base)
    case = create_case(mutation)
    return Individual(case)


def create_case(mutation):
    return "".join(mutation)


def generation_mutate(gen):
    fittest = select_fittest(gen)
    new_population = []
    for x in range(population_size):
        new_population.append(individual_mutate(fittest))
    return Generation(new_population)


def insert_random(base):
    mutation = base
    for index, char in enumerate(mutation):
        if mutation[index] == "":
            mutation[index] = random_string(1)
    return mutation


def random_select(fittest):
    to_select = random_number()
    extracted = []
    for count in range(to_select):
        value = random.choice(fittest.case)
        index = fittest.case.index(value)
    return extracted


def get_match(fittest):
    extracted = []
    for index, char in enumerate(fittest.case):
        if char == target[index]:
            extracted.append({"val": char, "ind": index})
    return extracted


def create_base(extracted):
    base = [""]*len(target)
    for item in extracted:
        base[item["ind"]] = item["val"]
    return base


def random_number():
    return random.randint(1, len(target)-1)


def select_fittest(gen):
    max = 0
    fittest = None
    for individual in gen.individuals:
        if individual.score > max:
            max = individual.score
            fittest = individual
    if fittest is None:
        fittest = random.choice(gen.individuals)
    print "fittest is: '{}' with score {}".format(fittest.case, fittest.score)
    return fittest


def calculate_fitness(guess, solution):
    fitness = 0
    for index, item in enumerate(guess):
        if item == solution[index]:
            fitness += 1
    if fitness == len(target):
        conclusion(guess)
    return fitness


def conclusion(guess):
    print "\n---\nIndividual: {}\nSolution: {}".format(guess, target)
    print "{} individuals were created.".format(Individual.ind_count)
    print "{} generations to reach the target.\n---".format(
        Generation.gen_count)
    exit()


def execute():
    current_gen = Generation()
    next_gen = current_gen
    for x in range(test_length):
        temp = next_gen
        next_gen = generation_mutate(current_gen)
        current_gen = temp
    return 0

if __name__ == "__main__":
    execute()
