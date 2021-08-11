# Project Description
In this project, the objective is to build a policy to solve the lunarlander-v2 with more than 200 points averaged with 100 consecutive runs. To achieve the goal, the writer applied Deep Q-network (DQN) as the action-value function estimator and the -greedy algorithm to get the optimal policy. Training and test results for the trained DQNs are presented in this report. Additionally, discussions on DQN hyperparameters are provided, including studies on the number of nodes in hidden layers, the learning rate, the size of replay memory pool, and the maximum step allowed for each episode.
# Instructions
In this folder, the main code includes:
- DQN-128 nodes.py: code used to train DQN;
- test.py: run test on trained DQN models;
Instrutors can run the DQN-128 nodes.py to train the model and test.py file to test.
# Collected data and trained models
There are 5 other folders included in this directory to save the collected data and trained models:
- Finished: this stores trained models and data collected during training and testing;
- learning rate: includes models and data used for learning rate parametric studies;
- Number of nodes: includes models and data used for the number of nodes parametric studies;
- replay_max_step: includes models and data used for parametric studies on the maximum step size in each episode;
- replay_pool_size: includes models and data used for parametric studies on the maximum length of replay memory pool.

Have fun!
