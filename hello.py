import string
import random
from collections import Counter

population_size = 10
test_length = 50
target = "Hello world"


class Individual:
    '''
        Representation of one case/score pair. Upon creation, fitness
        is calculated and applied as the score.
        Case can be manually defined. Default will generate a random string.
    '''

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
    '''
        Representation of a grouping of Individuals. Helper functions allow
        easier printing.
    '''

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


# Currently Unused
def random_select(fittest):
    '''
        Instead of selecting only the matched values,
        function will randomly select from string using
        random.choice().
    '''
    to_select = random_number()
    extracted = []
    for count in range(to_select):
        value = random.choice(fittest.case)
        index = fittest.case.index(value)
    return extracted


def random_number():
    '''
        Returns a random integer bewteen 1 and length of target-1.
    '''
    return random.randint(1, len(target)-1)


def calculate_fitness(guess, solution):
    '''
        Calculates fitness based on matching values at matching positions.
    '''
    fitness = 0
    for index, item in enumerate(guess):
        if item == solution[index]:
            fitness += 1
    if fitness == len(target):
        conclusion(guess)
    return fitness


def get_match(fittest):
    '''
        Extracts matching values and stores value and index location in a
        dictionary to be used to construct mutation.
    '''
    extracted = []
    for index, char in enumerate(fittest.case):
        if char == target[index]:
            extracted.append({"val": char, "ind": index})
    return extracted


def create_base(extracted):
    '''
        Creates an array as the base of the mutation by inserting previously
        extracted values.
    '''
    base = [""]*len(target)
    for item in extracted:
        base[item["ind"]] = item["val"]
    return base


def insert_random(base):
    '''
        Inserts random characters into empty indices of mutation base.
    '''
    mutation = base
    for index, char in enumerate(mutation):
        if mutation[index] == "":
            mutation[index] = random_string(1)
    return mutation


def create_case(mutation):
    '''
        Joins the array to form the case.
    '''
    return "".join(mutation)


def individual_mutate(fittest):
    '''
        Mutates a string. First finds matching values with target string and
        extracts position of those matching values. Then constructs an array
        of empty strings with length of target. Inserts matched values into
        the array and generates random characters to fill indices which are
        empty. Finally joins array to create a mutated string.
    '''
    extracted = get_match(fittest)
    base = create_base(extracted)
    mutation = insert_random(base)
    case = create_case(mutation)
    return Individual(case)


def select_fittest(gen):
    '''
        Finds the individual within a generation with the highest fitness.
    '''
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


def generation_mutate(gen):
    '''
        Finds the fittest individual, then creates a population of
        mutated individuals with which to fill a new generation.
    '''
    fittest = select_fittest(gen)
    new_population = []
    for x in range(population_size):
        new_population.append(individual_mutate(fittest))
    return Generation(new_population)


def conclusion(guess):
    '''
        Called when an individual is created and evaluated with the highest
        fitness level, indicating that the individual matches the target
        string. Lists details of the test and exits.
    '''
    print "\n---\nIndividual: {}\nSolution: {}".format(guess, target)
    print "{} individuals were created.".format(Individual.ind_count)
    print "{} generations to reach the target.\n---".format(
        Generation.gen_count)
    exit()


def execute():
    '''
        Creates a random generation. Then runs test for test_length 
        generations. Repeatedly mutates new generations using the previous as
        the base case.
    '''
    current_gen = Generation()
    next_gen = current_gen
    for x in range(test_length):
        temp = next_gen
        next_gen = generation_mutate(current_gen)
        current_gen = temp
    return 0

if __name__ == "__main__":
    execute()
