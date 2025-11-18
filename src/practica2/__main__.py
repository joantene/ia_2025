import gymnasium as gym

"""-Env.step(action): Executa un pas de temps de la dinàmica de l'entorn utilitzant les accions de l'agent.
-Env.reset(): Reinicia l'entorn a un estat intern inicial, retornant una observació i informació inicial.
-Env.action_space: L'objecte Space corresponent a les accions vàlides; totes les accions vàlides han d'estar contingudes dins de l'espai.
.Env.action_space.sample(): Mostreja aleatòriament un element d'aquest espai."""

def __main__():
    env = gym.make("FrozenLake-v1", is_slippery=True)
    