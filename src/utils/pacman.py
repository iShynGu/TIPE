import gym
import numpy as np
from scipy.spatial import distance

PACMAN_COLOR = np.array([210, 164, 74])
GHOST_COLOR = np.array([200, 72, 72])

def get_positions(state, color):
    positions = np.argwhere(np.all(state == color, axis=-1))
    return positions

# créer l'environnement
env = gym.make('MsPacman-v0', render_mode='human')

# réinitialiser l'environnement
state = env.reset()

done = False
while not done:
    position_pac = get_positions(state, PACMAN_COLOR)
    position_ghost = get_positions(state, GHOST_COLOR)

    if len(position_pac) > 0 and len(position_ghost) > 0:
        # Calculer les distances entre Pac-Man et chaque fantôme
        distances = distance.cdist(position_pac, position_ghost, 'euclidean')
        min_distance = np.min(distances)
        print(min_distance)
        # Calculer les distances pour chaque action possible
        possible_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        move_distances = [np.min(distance.cdist(position_pac + move, position_ghost, 'euclidean')) for move in possible_moves]

        # Choisir l'action qui maximise la distance
        action = np.argmax(move_distances) +1
    else:
        action = 0

    state, reward, done, info,_ = env.step(action)
    env.render()

env.close()