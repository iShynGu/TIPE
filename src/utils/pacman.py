import gym
import numpy as np
from scipy.spatial import distance

PACMAN_COLOR = np.array([210, 164, 74])
GHOSTS_COLOR = np.array([[200, 72, 72], [84, 184, 153], [180, 122, 48], [200, 72, 72]])
#changer la 4e couleur
WALL_COLOR=np.array([228,111,111])


def get_positions(state, color):
    positions = np.argwhere(np.all(state == color, axis=-1))
    return positions

def check_collision(state, position, direction):
    for i in range(1, 21):
        next_position = position + (i * np.array(direction))
        if np.all(state[next_position[0], next_position[1]] == WALL_COLOR):
            return True
    return False

env = gym.make('MsPacman-v0', render_mode='human')
state = env.reset()

done = False
while not done:
    print(state)
    position_pac = get_positions(state, PACMAN_COLOR)
    position_ghost = []
    for ghost in GHOSTS_COLOR:
        position_ghost.append(get_positions(state, ghost))

    position_ghost = np.concatenate(position_ghost)

    if len(position_pac) > 0 and len(position_ghost) > 0:
        distances = distance.cdist(position_pac, position_ghost, 'euclidean')
        min_distance = np.min(distances)
        print(min_distance)
        possible_moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        move_distances = []
        for move in possible_moves:
            if not check_collision(state, position_pac[0], move):
                move_distances.append(
                    np.min(distance.cdist(position_pac + 10*np.array(move), position_ghost, 'euclidean')))
            else:
                move_distances.append(0)

        action = np.argmax(move_distances) + 1
    else:
        action = 0

    state, reward, done, info, _ = env.step(action)
    env.render()

env.close()
