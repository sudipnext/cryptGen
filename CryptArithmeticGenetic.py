"""
Credits:
This code is a Python implementation of a cryptarithmetic solver.
Inspired by the GitHub repository: vkmgeek/Cryptarithmatic.

Current Implementation Author:
Sudip Parajuli
@sudipnext
coc42060@gmail.com
"""

import random
import re


class CryptarithmeticSolver:
    def __init__(self, puzzle):
        # converts all the letters to uppercase initially
        self.puzzle = puzzle.upper()
        # finds all the distinct letters in the puzzle
        self.letters = list(set(re.findall(r'[A-Z]', self.puzzle)))
        # finds the first letter of each word in the puzzle
        self.first_letters = set(
            word[0] for word in re.findall(r'[A-Z]+', self.puzzle))
        # initializing the population size, mutation rate, mutation decay and generations
        self.population_size = 100000
        self.mutation_rate = 0.01
        self.mutation_decay = 0.99
        self.generations = 1000

        if len(self.letters) > 10:
            raise ValueError(
                "Too many distinct letters, should be 10 or fewer.")

        left_side, right_side = self.puzzle.split('=')
        max_len_operand = max(map(len, re.findall(r'[A-Z]+', left_side)))
        if len(right_side.strip()) < max_len_operand or len(right_side.strip()) > max_len_operand + 1:
            raise ValueError(
                "Invalid puzzle: length of answer should be same or one more than the longest operand.")

    def fitness(self, chromosome):
        """
        Returns the fitness of a chromosome.
        The fitness is the absolute difference between the left side of the equation
        and the right side of the equation.
        Inputs:
        chromosome (list): A list of digits representing a possible solution.
        Returns:
        float: The fitness of the chromosome

        """
        # mapping the letters to the digits in the chromosome
        mapping = dict(zip(self.letters, chromosome))
        # check if any of the operator1 or operator2 or answer starts with 0
        if any(mapping[letter] == 0 for letter in self.first_letters):
            return float('inf')

        # try to evaluate the expression with the given mapping
        try:
            expr = self.puzzle
            for letter, digit in mapping.items():
                expr = expr.replace(letter, str(digit))
            left, right = expr.split('=')
            return abs(eval(left) - eval(right))
        except:
            return float('inf')

    def create_chromosome(self):
        """
        Creates a random chromosome.
        Inputs: None 
        Returns:
        list: A list of digits from 

        """
        return random.sample(range(10), len(self.letters))

    def crossover(self, parent1, parent2):
        """
        Performs crossover between two parents.
        Inputs:
        parent1 (list): A list of digits representing the first parent.
        parent2 (list): A list of digits representing the second parent.
        Returns:
        list: A list of digits representing the child chromosome.

        """
        # splitting the parents at a random index and then performing crossover example parent1 = [1,2,3,4,5] parent2 = [6,7,8,9,0] would be split at 3 and the child would be [1,2,3,9,0]
        split = random.randint(0, len(self.letters) - 1)
        # child would be the first half of parent1 and the second half of parent2
        child = parent1[:split] + parent2[split:]
        # checking if any of the digits are repeated in the child and then replacing it with a random digit
        used_digits = set(child[:split])
        # looping through the second half of the child and checking if any of the digits are repeated
        for i in range(split, len(child)):
            # if the digit is repeated then replace it with a random digit
            if child[i] in used_digits:
                unused_digits = set(range(10)) - used_digits
                child[i] = random.choice(list(unused_digits))
            used_digits.add(child[i])
        return child

    def mutate(self, chromosome):
        """
        Mutates a chromosome by swapping two random digits.
        Inputs:
        chromosome (list): A list of digits representing the chromosome.
        Returns:
        list: A list of digits representing the mutated chromosome.

        """
        # performing mutation by swapping two random digits in the chromosome with a probability of mutation_rate
        # random.random returns a random float between 0.0 and 1.0
        if random.random() < self.mutation_rate:
            # selecting two random indices in the chromosome and then swapping them
            i, j = random.sample(range(len(chromosome)), 2)
            chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
        return chromosome

    def solve(self):
        """
        Solves the cryptarithmetic puzzle.
        Inputs: None
        Returns:
        dict: A mapping of letters to digits if a solution is found, None otherwise.

        """

        # initializing the population with random chromosomes i.e digits from 0 to 9 which is in nested list
        population = [self.create_chromosome()
                      for _ in range(self.population_size)]

        # looping through the generations
        for generation in range(self.generations):
            # sorting the population based on the fitness
            population = sorted(population, key=self.fitness)
            # getting the best fitness
            best_fitness = self.fitness(population[0])

            # if the best fitness is 0 then return the mapping of letters to digits
            if best_fitness == 0:
                return dict(zip(self.letters, population[0]))

            # printing the best fitness for every 100 generations
            if generation % 100 == 0:
                print(
                    f"Generation {generation}: Best fitness = {best_fitness}")

            # creating a new population by selecting the top 2 chromosomes and then performing crossover and mutation
            new_population = population[:2]
            # looping through the population and performing crossover and mutation
            while len(new_population) < self.population_size:
                # selecting the top 50 chromosomes and then selecting 2 random chromosomes from it
                parent1, parent2 = random.choices(population[:50], k=2)
                # performing crossover and mutation
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                # appending the child to the new population
                new_population.append(child)
            # updating the population with the new population
            population = new_population
            # updating the mutation rate by multiplying it with mutation decay
            self.mutation_rate *= self.mutation_decay

        return None

    def print_solution(self, solution):
        """
        Prints the solution if found.
        Inputs:
        solution (dict): A mapping of letters to digits.
        Returns: None

            """
        if solution:
            print("Solution found:")
            for letter, digit in solution.items():
                print(f"{letter} = {digit}")
            solved_equation = ''.join(str(solution.get(char, char))
                                      for char in self.puzzle)
            print(f"Solved equation: {solved_equation}")
        else:
            print("No solution found")


# # Example usage
# puzzle = "SEND + MORE = MONEY"
# solver = CryptarithmeticSolver(puzzle)
# solution = solver.solve()
# solver.print_solution(solution)
