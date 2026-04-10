import random
import string
import re
import math

# ── Character pool ────────────────────────────────────────────────────────────
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS    = string.digits
SYMBOLS   = "!@#$%^&*()_+-=[]{}|;:,.<>?"
ALL_CHARS = LOWERCASE + UPPERCASE + DIGITS + SYMBOLS

N_CHARS        = len(ALL_CHARS)
PASSWORD_LENGTH = 12

# ── Fitness / heuristic ───────────────────────────────────────────────────────
def fitness(password: str) -> float:
    """Same strength metric used in the GA file."""
    score = 0.0
    length = len(password)

    score += min(length * 2.5, 30)

    has_lower  = bool(re.search(r'[a-z]', password))
    has_upper  = bool(re.search(r'[A-Z]', password))
    has_digit  = bool(re.search(r'[0-9]', password))
    has_symbol = bool(re.search(r'[^a-zA-Z0-9]', password))
    score += sum([has_lower, has_upper, has_digit, has_symbol]) * 10

    unique_ratio = len(set(password)) / max(length, 1)
    score += unique_ratio * 20

    repeats = sum(1 for i in range(length - 1) if password[i] == password[i+1])
    score -= repeats * 2

    sequentials = sum(
        1 for i in range(length - 2)
        if ord(password[i+1]) - ord(password[i]) == 1
        and ord(password[i+2]) - ord(password[i+1]) == 1
    )
    score -= sequentials * 3

    return max(score, 0.0)

def heuristic(char: str) -> float:
    """
    Per-character heuristic: how much strength does this character class add?
    Symbols > Digits > Uppercase > Lowercase.
    """
    if char in SYMBOLS:   return 4.0
    if char in DIGITS:    return 3.0
    if char in UPPERCASE: return 2.0
    return 1.0

# ── ACO core ──────────────────────────────────────────────────────────────────
class AntColonyPasswordOptimizer:
    """
    Pheromone matrix shape: (PASSWORD_LENGTH, N_CHARS)
    pheromone[pos][char_idx] = desirability of placing char at position pos
    """

    def __init__(
        self,
        n_ants:        int   = 50,
        n_iterations:  int   = 100,
        alpha:         float = 1.0,   # pheromone weight
        beta:          float = 2.0,   # heuristic weight
        evaporation:   float = 0.5,   # rho  – evaporation rate
        Q:             float = 100.0, # pheromone deposit constant
        tau_init:      float = 1.0,   # initial pheromone level
    ):
        self.n_ants       = n_ants
        self.n_iterations = n_iterations
        self.alpha        = alpha
        self.beta         = beta
        self.evaporation  = evaporation
        self.Q            = Q

        # Pheromone matrix initialised uniformly
        self.pheromone = [
            [tau_init] * N_CHARS for _ in range(PASSWORD_LENGTH)
        ]
        # Pre-compute heuristic values (constant)
        self.heuristics = [heuristic(c) for c in ALL_CHARS]

    def _build_password(self) -> str:
        """One ant constructs a password character by character."""
        password = []
        for pos in range(PASSWORD_LENGTH):
            # Probability ∝ τ^α · η^β
            weights = [
                (self.pheromone[pos][ci] ** self.alpha) *
                (self.heuristics[ci] ** self.beta)
                for ci in range(N_CHARS)
            ]
            total = sum(weights)
            probabilities = [w / total for w in weights]

            # Roulette-wheel selection
            r = random.random()
            cumulative = 0.0
            chosen_idx = N_CHARS - 1
            for ci, p in enumerate(probabilities):
                cumulative += p
                if r <= cumulative:
                    chosen_idx = ci
                    break

            password.append(ALL_CHARS[chosen_idx])
        return ''.join(password)

    def _update_pheromones(self, ants: list[tuple[str, float]]) -> None:
        """Evaporate then deposit pheromones based on fitness."""
        # Evaporation
        for pos in range(PASSWORD_LENGTH):
            for ci in range(N_CHARS):
                self.pheromone[pos][ci] *= (1.0 - self.evaporation)
                self.pheromone[pos][ci] = max(self.pheromone[pos][ci], 0.01)

        # Deposit
        for pwd, score in ants:
            deposit = self.Q * score / 100.0  # normalise deposit
            for pos, char in enumerate(pwd):
                ci = ALL_CHARS.index(char)
                self.pheromone[pos][ci] += deposit

    def run(self) -> str:
        best_password = ""
        best_score    = -1.0

        for iteration in range(self.n_iterations):
            # All ants build a solution
            ants = []
            for _ in range(self.n_ants):
                pwd   = self._build_password()
                score = fitness(pwd)
                ants.append((pwd, score))

            # Update best
            iter_best_pwd, iter_best_score = max(ants, key=lambda x: x[1])
            if iter_best_score > best_score:
                best_score    = iter_best_score
                best_password = iter_best_pwd

            # Pheromone update
            self._update_pheromones(ants)

            if iteration % 25 == 0 or iteration == self.n_iterations - 1:
                print(f"  Iter {iteration:>3}  |  Best fitness: {best_score:.2f}  |  Password: {best_password}")

        return best_password

# ── Comparison helper ─────────────────────────────────────────────────────────
def compare_with_random(n: int = 10) -> None:
    print("\n── Random passwords (baseline) ──")
    random_scores = []
    for _ in range(n):
        pwd   = ''.join(random.choices(ALL_CHARS, k=PASSWORD_LENGTH))
        score = fitness(pwd)
        random_scores.append(score)
        print(f"  {pwd}  →  score: {score:.2f}")
    print(f"\n  Avg random score: {sum(random_scores)/len(random_scores):.2f}")

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print(" Ant Colony Optimization – Secure Password Generation")
    print("=" * 55)

    aco = AntColonyPasswordOptimizer(
        n_ants       = 50,
        n_iterations = 100,
        alpha        = 1.0,
        beta         = 2.0,
        evaporation  = 0.5,
        Q            = 100.0,
    )

    print("\nAnts building passwords…\n")
    best = aco.run()

    print(f"\n✓ Best ACO password : {best}")
    print(f"  Fitness score     : {fitness(best):.2f}")

    compare_with_random(n=10)