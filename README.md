# DP and Learning Model for Taxi Domain 

#### `problem statement` 
Consider the Taxi Domain problem that involves controlling a taxi agent that can pick up and drop passengers in a grid world. model this problem as a sequential decision-making problem to implement two algorithms for finding a good policy. the algorithms are - 
* Dynamic programming (offline learning) -  model the taxi domain as a Markov Decision Process (MDP) and compute optimal policy for the taxi agent using value-iteration and policy iteration algorithms.
* Reinforcement learning methods (online learning) - incorporate RL (Q and SARSA learning) on an unknown taxi domain MDP where the transition model and the reward model is not known to the taxi agent. In this case, the taxi must act only based on its past experience. \
__complete problem statement is given in file named 'ProblemStatement'.__


#### `Implementation`
* Formulated a MDP Model for sequential decision making for given 5x5 and 10x10 grid type taxi domain.
* Implemented Value-Iteration and Policy Iteration and found optimal policy using convergence of Policy iteration.
* Incorporated diferent learning Model like Q-Learning and SARSA on an unknown taxi domain for finding Optimal Policy



