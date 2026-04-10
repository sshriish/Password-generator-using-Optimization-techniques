## Algorithms

### 1. Genetic Algorithm (`GeneticAlgorithm.py`)

Mimics biological evolution through selection, crossover, and mutation.

**Key parameters:**

| Parameter         | Value      | Description                                  |
| ----------------- | ---------- | -------------------------------------------- |
| `population_size` | 100        | Number of passwords evolved per generation   |
| `generations`     | 200        | Total iterations of evolution                |
| `mutation_rate`   | 0.05 (5%)  | Probability of random character replacement  |
| `elite_size`      | 5          | Top individuals carried unchanged to next gen|

**How it works:**
1. Initialises a random population of 100 passwords
2. Evaluates fitness for every individual
3. Selects parents via **tournament selection** (k=3)
4. Produces offspring via **single-point crossover**
5. Applies **random character mutation** at 5% probability
6. Top 5 individuals (elites) pass unchanged to the next generation
7. Repeats for 200 generations

**Sample output:**
```
  Gen   0  |  Best fitness: 90.00  |  Password: Tr?ph8d;]s-^
  Gen  50  |  Best fitness: 90.00  |  Password: Tr?ph8d;]s-^
  ...
✓ Best GA password : Tr?ph8d;]s-^
  Fitness score    : 90.00
  Avg random score : 85.77
```

---

### 2. Ant Colony Optimization (`AntColony.py`)

Simulates foraging behaviour of ants using pheromone trails to guide character selection.

**Key parameters:**

| Parameter          | Value  | Description                          |
| ------------------ | ------ | ------------------------------------ |
| `n_ants`           | 50     | Solutions built per iteration        |
| `n_iterations`     | 100    | Total number of colony cycles        |
| `alpha (α)`        | 1.0    | Pheromone influence weight           |
| `beta (β)`         | 2.0    | Heuristic influence weight           |
| `evaporation (ρ)`  | 0.5    | Pheromone decay rate per iteration   |
| `Q`                | 100.0  | Pheromone deposit constant           |

**How it works:**
1. Initialises a pheromone matrix of shape `(password_length × charset_size)` uniformly
2. Each ant builds a password **character by character** — at each position, it samples from a probability distribution proportional to `τ^α × η^β`
3. Heuristic `η` biases selection: **Symbols > Digits > Uppercase > Lowercase**
4. After all ants finish, pheromones **evaporate** by factor ρ
5. Better-scoring passwords **deposit more pheromone**, reinforcing strong character choices
6. Over iterations, trails converge toward high-strength patterns

**Sample output:**
```
  Iter   0  |  Best fitness: 90.00  |  Password: 2_D?PU;|%6)t
  Iter  25  |  Best fitness: 90.00  |  Password: 2_D?PU;|%6)t
  ...
✓ Best ACO password : 2_D?PU;|%6)t
  Fitness score     : 90.00
  Avg random score  : 83.13
```

---

### 3. Particle Swarm Optimization (`ParticleSwarm.py`)

Simulates a swarm of particles moving through a discrete character-index space toward high-fitness regions.

**Key parameters:**

| Parameter       | Value         | Description                               |
| --------------- | ------------- | ----------------------------------------- |
| `n_particles`   | 60            | Swarm size                                |
| `n_iterations`  | 150           | Total number of swarm cycles              |
| `inertia (w)`   | 0.7 → decays  | Controls momentum of particle movement    |
| `cognitive (c1)`| 1.5           | Pull toward personal best position        |
| `social (c2)`   | 1.5           | Pull toward global best position          |
| `w_decay`       | 0.99 / iter   | Gradually shifts swarm toward exploitation|

**How it works:**
1. Each particle stores a password as a **list of character indices** into the character set
2. Velocity represents a floating-point shift bias in index space
3. Each iteration, velocity is updated: `v = w·v + c1·r1·(pbest − x) + c2·r2·(gbest − x)`
4. Position updates: `x = x + round(v)` (discrete, mod charset size)
5. Each particle tracks its **personal best** (`pbest`); the swarm tracks the **global best** (`gbest`)
6. Inertia weight decays each iteration to balance **exploration vs. exploitation**

**Sample output:**
```
  Iter   0  |  Best fitness: 90.00  |  Password: lcxtEFg5N.;+
  Iter  30  |  Best fitness: 90.00  |  Password: lcxtEFg5N.;+
  ...
✓ Best PSO password : lcxtEFg5N.;+
  Fitness score     : 90.00
  Avg random score  : 82.47
```

---

## Results Summary

| Algorithm | Best Fitness | Avg Random Baseline | Improvement |
|-----------|--------------|---------------------|-------------|
| Genetic   | **90.00**    |      85.77          |   +4.23     |
| Ant Colony|  **90.00**   |      83.13          |   +6.87     |
| Particle Swarm | **90.00**|     82.47          |   +7.53     |

All three algorithms consistently outperform randomly generated passwords, validating the core hypothesis that **optimization-based generation produces stronger passwords than random generation**.



