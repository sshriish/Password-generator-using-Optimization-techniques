import random
import string
import re

# ── Character pool ──────────────────────────────────────────────────────────
LOWERCASE   = string.ascii_lowercase          # a-z
UPPERCASE   = string.ascii_uppercase          # A-Z
DIGITS      = string.digits                   # 0-9
SYMBOLS     = "!@#$%^&*()_+-=[]{}|;:,.<>?"   # special chars
ALL_CHARS   = LOWERCASE + UPPERCASE + DIGITS + SYMBOLS

PASSWORD_LENGTH = 12   # target password length

# ── Fitness function ─────────────────────────────────────────────────────────
def fitness(password: str) -> float:
    """
    Evaluate password strength on a 0-100 scale.
    Criteria:
      - Length bonus
      - Character diversity (lower, upper, digit, symbol)
      - Penalty for repeated characters
      - Penalty for sequential patterns
    """
    score = 0.0
    length = len(password)

    # 1. Length score (up to 30 pts)
    score += min(length * 2.5, 30)

    # 2. Character class diversity (up to 40 pts)
    has_lower  = bool(re.search(r'[a-z]', password))
    has_upper  = bool(re.search(r'[A-Z]', password))
    has_digit  = bool(re.search(r'[0-9]', password))
    has_symbol = bool(re.search(r'[^a-zA-Z0-9]', password))
    score += sum([has_lower, has_upper, has_digit, has_symbol]) * 10

    # 3. Unique character ratio (up to 20 pts)
    unique_ratio = len(set(password)) / max(length, 1)
    score += unique_ratio * 20

    # 4. Penalty for repeated consecutive chars
    repeats = sum(1 for i in range(length - 1) if password[i] == password[i+1])
    score -= repeats * 2

    # 5. Penalty for sequential patterns (abc, 123)
    sequentials = sum(
        1 for i in range(length - 2)
        if ord(password[i+1]) - ord(password[i]) == 1
        and ord(password[i+2]) - ord(password[i+1]) == 1
    )
    score -= sequentials * 3

    return max(score, 0.0)   # never negative

# ── GA operators ─────────────────────────────────────────────────────────────
def random_password(length: int = PASSWORD_LENGTH) -> str:
    return ''.join(random.choices(ALL_CHARS, k=length))

def selection(population: list[str], fitnesses: list[float], k: int = 3) -> str:
    """Tournament selection: pick best from k random candidates."""
    candidates = random.choices(range(len(population)), k=k)
    best = max(candidates, key=lambda i: fitnesses[i])
    return population[best]

def crossover(parent1: str, parent2: str) -> tuple[str, str]:
    """Single-point crossover."""
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(password: str, mutation_rate: float = 0.05) -> str:
    """Randomly replace characters with given probability."""
    pwd = list(password)
    for i in range(len(pwd)):
        if random.random() < mutation_rate:
            pwd[i] = random.choice(ALL_CHARS)
    return ''.join(pwd)

# ── Main GA loop ──────────────────────────────────────────────────────────────
def genetic_algorithm(
    population_size: int = 100,
    generations:     int = 200,
    mutation_rate:   float = 0.05,
    elite_size:      int = 5,
) -> str:
    # Initialise random population
    population = [random_password() for _ in range(population_size)]

    best_password = ""
    best_fitness  = -1.0

    for gen in range(generations):
        fitnesses = [fitness(p) for p in population]

        # Track global best
        gen_best_idx = max(range(len(fitnesses)), key=lambda i: fitnesses[i])
        if fitnesses[gen_best_idx] > best_fitness:
            best_fitness  = fitnesses[gen_best_idx]
            best_password = population[gen_best_idx]

        if gen % 50 == 0 or gen == generations - 1:
            print(f"  Gen {gen:>3}  |  Best fitness: {best_fitness:.2f}  |  Password: {best_password}")

        # Elitism – carry top individuals unchanged
        sorted_pop = [p for _, p in sorted(zip(fitnesses, population), reverse=True)]
        new_population = sorted_pop[:elite_size]

        # Fill rest of population via crossover + mutation
        while len(new_population) < population_size:
            p1 = selection(population, fitnesses)
            p2 = selection(population, fitnesses)
            c1, c2 = crossover(p1, p2)
            new_population.append(mutate(c1, mutation_rate))
            if len(new_population) < population_size:
                new_population.append(mutate(c2, mutation_rate))

        population = new_population

    return best_password

# ── Comparison: GA vs random ──────────────────────────────────────────────────
def compare_with_random(n: int = 10) -> None:
    print("\n── Random passwords ──")
    random_scores = []
    for _ in range(n):
        pwd = random_password()
        score = fitness(pwd)
        random_scores.append(score)
        print(f"  {pwd}  →  score: {score:.2f}")

    print(f"\n  Avg random score: {sum(random_scores)/len(random_scores):.2f}")

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print(" Genetic Algorithm – Secure Password Generation")
    print("=" * 55)

    print("\nEvolving population…\n")
    best = genetic_algorithm(population_size=100, generations=200, mutation_rate=0.05)

    print(f"\n✓ Best GA password : {best}")
    print(f"  Fitness score    : {fitness(best):.2f}")

    compare_with_random(n=10)