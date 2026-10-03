Snake AI: A Comparative Evaluation of Search, Heuristic, and Reinforcement Learning Agents


The purpose of this project is first to develop a clean, organized classic snake game in pygame. Multiple artificial intelligence agents are then coded from scratch to play the snake game. The performance of each of these agents are benchmarked and compared to one another.

The individual AI agents include:

- Random

This simple agent acts as a control group. The agent produces a random decision that results in a low score.

- Hamiltonian Cycle

The Hamiltonian cycle visits every single possible coordinate once and returns to the exact same spot. This allows the agent to obtain a perfect score every try. Although it gets a perfect score, it is extremely inefficient. 

- Rule Based

This is agent is the start of AI decision-making by using simple rules to guide the AI. The code that was implemented produces a list of legal moves that the snake can use without dying. The AI then picks the move that allows the snake to reach the apple.

- Heuristic

This agent uses heuristics to calculate the best possible move in a certain situation. The heuristics give every legal move that can be used a score based on different conditions, the move with the highest score is then chosen for the snake to use. The 5 main heuristics that were used include 



Skills used:

- Python 3

- Git/Github

- Pygame

- Advanced Pathfinding Algorithms

- PyTorch




Author:

Isaac Oliver