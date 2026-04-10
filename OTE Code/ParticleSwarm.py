import random
import string
import re
import copy

# ── Character pool ────────────────────────────────────────────────────────────
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS    = string.digits
SYMBOLS   = "!@#$%^&*()_+-=[]{}|;:,.<>?"
ALL_CHARS = LOWERCASE + UPPERCASE + DIGITS + SYMBOLS

N_CHARS         = len(ALL_CHARS)
PASSWORD_LENGTH = 12

# ── Fitness function (shared metric) ─────────────────────────────────────────
def fitness(password: str) -> float:
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

# ── Particle ──────────────────────────────────────────────────────────────────
class Particle:
    """
    Position  : list of N integer indices into ALL_CHARS  (one per position)
    Velocity  : list of N floats – interpreted as a "shift bias" in index space.
                During update, a stochastic rule decides whether to move the
                index toward pbest / gbest by some velocity amount.
    """

    def __init__(self):
        # Random starting position (character indices)
        self.position  = [random.randint(0, N_CHARS - 1) for _ in range(PASSWORD_LENGTH)]
        # Velocity initialised near zero
        self.velocity  = [random.uniform(-N_CHARS * 0.1, N_CHARS * 0.1)
                          for _ in range(PASSWORD_LENGTH)]
        self.pbest_pos = copy.copy(self.position)
        self.pbest_fit = self._evaluate()

    def _evaluate(self) -> float:
        return fitness(self.to_string())

    def to_string(self) -> str:
        return ''.join(ALL_CHARS[idx % N_CHARS] for idx in self.position)

    def update_velocity(
        self,
        gbest_pos: list[int],
        w:  float,   # inertia weight
        c1: float,   # cognitive coefficient
        c2: float,   # social coefficient
    ) -> None:
        for i in range(PASSWORD_LENGTH):
            r1, r2 = random.random(), random.random()
            cognitive = c1 * r1 * (self.pbest_pos[i] - self.position[i])
            social    = c2 * r2 * (gbest_pos[i]      - self.position[i])
            self.velocity[i] = w * self.velocity[i] + cognitive + social

            # Clamp velocity to avoid explosion
            max_v = N_CHARS * 0.3
            self.velocity[i] = max(-max_v, min(max_v, self.velocity[i]))

    def update_position(self) -> None:
        for i in range(PASSWORD_LENGTH):
            # Discrete move: round velocity to nearest integer step
            self.position[i] = int(self.position[i] + round(self.velocity[i])) % N_CHARS

        current_fit = self._evaluate()
        if current_fit > self.pbest_fit:
            self.pbest_fit = current_fit
            self.pbest_pos = copy.copy(self.position)

# ── PSO main loop ─────────────────────────────────────────────────────────────
def particle_swarm_optimization(
    n_particles: int   = 60,
    n_iterations: int  = 150,
    w:  float = 0.7,    # inertia
    c1: float = 1.5,    # cognitive (personal best)
    c2: float = 1.5,    # social    (global best)
    w_decay: float = 0.99,  # gradually reduce inertia
) -> str:
    # Initialise swarm
    swarm = [Particle() for _ in range(n_particles)]

    # Global best
    gbest_particle = max(swarm, key=lambda p: p.pbest_fit)
    gbest_pos      = copy.copy(gbest_particle.pbest_pos)
    gbest_fit      = gbest_particle.pbest_fit

    for iteration in range(n_iterations):
        for particle in swarm:
            particle.update_velocity(gbest_pos, w, c1, c2)
            particle.update_position()

            if particle.pbest_fit > gbest_fit:
                gbest_fit = particle.pbest_fit
                gbest_pos = copy.copy(particle.pbest_pos)

        # Decay inertia weight
        w *= w_decay

        if iteration % 30 == 0 or iteration == n_iterations - 1:
            best_pwd = ''.join(ALL_CHARS[idx % N_CHARS] for idx in gbest_pos)
            print(f"  Iter {iteration:>3}  |  Best fitness: {gbest_fit:.2f}  |  Password: {best_pwd}")

    return ''.join(ALL_CHARS[idx % N_CHARS] for idx in gbest_pos)

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
    print(" Particle Swarm Optimization – Password Generation")
    print("=" * 55)

    print("\nSwarm searching…\n")
    best = particle_swarm_optimization(
        n_particles  = 60,
        n_iterations = 150,
        w  = 0.7,
        c1 = 1.5,
        c2 = 1.5,
    )

    print(f"\n✓ Best PSO password : {best}")
    print(f"  Fitness score     : {fitness(best):.2f}")

    compare_with_random(n=10)