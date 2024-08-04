from itertools import permutations

class CryptarithmeticSolver:
    def __init__(self, word1, word2, word3):
        self.digits = list(range(10))
        self.word1 = word1
        self.word2 = word2
        self.word3 = word3
        self.mapped_output = {}
    
    def word_to_number(self, word):
        number = 0
        for char in word:
            number = number * 10 + self.mapped_output[char]
        return number

    def check_solution(self):
        return self.word_to_number(self.word1) + self.word_to_number(self.word2) == self.word_to_number(self.word3)

    def solve(self):
        letters = set(self.word1 + self.word2 + self.word3)
        if len(letters) > 10:
            print("No solution possible due to too many unique letters.")
            return False

        for perm in permutations(self.digits, len(letters)):
            self.mapped_output = dict(zip(letters, perm))

            if self.mapped_output[self.word1[0]] == 0 or self.mapped_output[self.word2[0]] == 0 or self.mapped_output[self.word3[0]] == 0:
                continue

            if self.check_solution():
                print(f"Solution found: {self.mapped_output}")
                print(f"{self.word1} = {self.word_to_number(self.word1)}, {self.word2} = {self.word_to_number(self.word2)}, {self.word3} = {self.word_to_number(self.word3)}")
                return True

        print("No solution found.")
        return False

# # Usage example
# solver = CryptarithmeticSolver("LOGIC", "LOGIC", "PROLOG")
# solver.solve()
