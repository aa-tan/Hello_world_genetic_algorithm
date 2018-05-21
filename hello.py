import string
import random
from collections import Counter

population_size = 10
target = "Hello world"


class Individual:
    # global target

    def __init__(self, case=None):
        if case is None:
            self.case = random_string()
        else:
            self.case = case
        self.score = calculate_fitness(self.case, target)

    def __str__(self):
        return "Case: {}\nScore: {}".format(self.case, self.score)


def random_string(length=11, characters=string.ascii_lowercase):
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
        ret = ""
        for item in self.individuals:
            ret += "{}\n".format(item)
        return ret


def individual_mutate(fittest):
    extracted = random_select(fittest)
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
        if char is "":
            mutation[index] = random_string(1)
    return mutation


def random_select(fittest):
    to_select = random_number()
    extracted = []
    for count in range(to_select):
        value = random.choice(fittest.case)
        index = fittest.case.index(value)
        extracted.append({"val": value, "ind": index})
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
    return fittest


def fill_in_string():

    return 0


def calculate_fitness(guess, solution):
    guess_counter = Counter(guess)
    solution_counter = Counter(solution)
    fitness = 0
    for index, item in guess_counter.iteritems():
        fitness += min(item, solution_counter[index])
    for index, item in enumerate(guess):
        if item == solution[index]:
            fitness += 1
    if fitness == len(target)*2:
        print "guess: {}\nsolution: {}\n are the same".format(guess, solution)
        print "it took {} generations".format(Generation.gen_count)
        exit()
    return fitness


def recurse(gen):
    if Generation.gen_count > 100:
        print gen
        exit()
    next_gen = generation_mutate(gen)
    recurse(next_gen)


def execute():
    gen_1 = Generation()
    recurse(gen_1)
    return 0

if __name__ == "__main__":
    execute()
