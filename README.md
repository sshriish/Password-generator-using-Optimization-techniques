# Password-generator-using-Optimization-techniques
Secure Password Generation using Optimization Algorithms


📌 Overview
This project explores the use of metaheuristic optimization algorithms to generate strong and secure passwords. Instead of relying on naive random generation, we model password creation as an optimization problem, where the objective is to maximize password strength.

The project implements and compares three powerful optimization techniques:

Genetic Algorithm (GA)

Ant Colony Optimization (ACO)

Particle Swarm Optimization (PSO)


🎯 Objective
The goal is to:

Automatically generate high-strength passwords

Design a fitness function to evaluate password security

Compare optimization algorithms against random password generation

Demonstrate how optimization improves password quality

⚙️ Features
Custom fitness function (0–100 scale) based on:

Length

Character diversity (lowercase, uppercase, digits, symbols)

Uniqueness of characters

Penalties for repetition and sequential patterns

Implementation of 3 optimization algorithms

Comparison with random baseline

Modular and reusable code

🧠 Algorithms Implemented
1. Genetic Algorithm
Evolution-based approach

Uses:

Selection (Tournament)

Crossover (Single-point)

Mutation (Random replacement)

Includes elitism to preserve best solutions

📄 Code: 
GeneticAlgorithm


2. Ant Colony Optimization
Inspired by ant foraging behavior

Uses pheromone trails to guide character selection

Combines:

Pheromone influence (τ)

Heuristic importance (η)

📄 Code: 
AntColony


3. Particle Swarm Optimization
Swarm-based search algorithm

Each particle represents a password

Updates based on:

Personal best (pbest)

Global best (gbest)

📄 Code: 
ParticleSwarm


📊 Fitness Function (Core Idea)
The strength of a password is evaluated using:

Length score (max 30)

Character diversity (max 40)

Unique character ratio (max 20)

Penalties:

Repeated characters

Sequential patterns (e.g., "abc", "123")

This ensures passwords are not just random, but structurally strong.

📈 Results Summary
Algorithm	Best Fitness	Random Baseline	Improvement
Genetic Algorithm	90.00	~85.77	+4.23
Ant Colony Optimization	90.00	~83.13	+6.87
Particle Swarm Optimization	90.00	~82.47	+7.53

📄 Detailed results: 
README_Output


🚀 How to Run
1. Clone the repository
Bash

git clone https://github.com/your-username/password-optimization.git
cd password-optimization
2. Run any algorithm
Bash

python GeneticAlgorithm.py
python AntColony.py
python ParticleSwarm.py
📂 Project Structure

├── GeneticAlgorithm.py
├── AntColony.py
├── ParticleSwarm.py
├── README.md
🧪 Example Output

Best password : Tr?ph8d;]s-^
Fitness score : 90.00
Avg random    : 85.77
⚠️ Limitations
Fitness function is heuristic-based (not cryptographically rigorous)

Does not account for:

Real-world password cracking techniques

Dictionary attacks

Fixed password length (12)

🔮 Future Improvements
Integrate machine learning-based scoring

Add adaptive password length

Incorporate real-world breach datasets

Hybrid algorithms (GA + PSO, etc.)

GUI or web interface

📚 Applications
Password managers

Security systems

Educational demonstration of optimization algorithms

Research in cybersecurity + AI

👤 Author
Shrish Sharan

📜 License
This project is for academic and educational purposes.


