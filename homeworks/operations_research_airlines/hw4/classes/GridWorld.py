import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from itertools import product
import numpy as np


class GridWorld:
    """
    Class for obtaining the optimal policy of the grid world using the policy iteration method
    """
    def __init__(self, grid, flags, gamma=0.9, theta=1e-4):
        self.grid = grid
        self.rows, self.cols = grid.shape
        self.flags = flags
        self.gamma = gamma
        self.theta = theta

        # Setup
        mask = ~np.isnan(self.grid)
        self.S = [tuple(s) for s in np.array(np.nonzero(mask)).T]
        self.A = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        # Initialization
        self.V = {s: 0 for s in self.S}
        self.pi = {s: self.A[0] for s in self.S}
        self.transition = self._get_transition_state_dict()
        self.P = self._get_transition_function_dict()


    def _collided(self, s):
        """
        Check if a state is out of bounds or collides with a wall (NaN)
        """
        return not (0 <= s[0] < self.rows and 0 <= s[1] < self.cols) or np.isnan(self.grid[s])


    def _bounce_back_states(self, s, possible_states):
        """
        Update possible next states if bounce back
        """
        fallback = possible_states[0]
        if self._collided(fallback):
            return [s] * len(possible_states)
        else:
            return [s if self._collided(_s) else _s for _s in possible_states]


    def _get_transition_state_dict(self):
        """
        Return a dictionary of possible next states given state s and action a
        """
        transition = {s: {} for s in self.S}
        
        # Define rotation functions
        def left(a): return (-a[1], a[0])
        def right(a): return (a[1], -a[0])
        
        # Precompute all possible state transitions
        for s, a in product(self.S, self.A):
            sa = np.array(s) + a
            # Generate possible states with bounce-back handling
            deltas = [(0, 0), left(a), right(a)]
            possible_states = [tuple(sa + d) for d in deltas]
            transition[s][a] = self._bounce_back_states(s, possible_states) 
        
        return transition


    def _get_transition_function_dict(self):
        """
        Return the transition probability function P(s'|s,a) as a dict
        """
        P = {s: {} for s in self.S}

        for s, a in product(self.S, self.A):
            next_states = self.transition[s][a]
            P[s][a] = {
                tuple(next_states[0]): 0.8,
                tuple(next_states[1]): 0.1,
                tuple(next_states[2]): 0.1
            }

        return P


    def _update_value(self, s, a):
        return sum(self.P[s][a][s_prime] * (self.grid[s_prime] + self.gamma*self.V[s_prime]) for s_prime in self.transition[s][a])
        

    def solve_grid_world(self, max_iterations=float('inf')):
        """
        Return optimal policy of grid world obtained by using the policy iteration method
        """
        i = 0
        while i < max_iterations:
            i += 1
            # Policy evaluation
            delta = 0
            for s in self.S:
                previous_value = self.V[s]
                self.V[s] = self._update_value(s, self.pi[s])
                delta = max(delta, abs(previous_value - self.V[s]))

            # Policy improvement
            policy_stable = True
            for s in self.S:
                previous_pi = self.pi[s]
                action_values = {tuple(a): self._update_value(s, a) for a in self.A}
                self.pi[s] = max(action_values, key=action_values.get)
                if previous_pi != self.pi[s]:
                    policy_stable = False

            # Stop in convergence
            if policy_stable and delta < self.theta:
                print(f"necessary iterations: {i}")
                return


    def show_grid(self):
        """
        Plot grid world
        """
        if not self.flags['plot']: return

        # Create a white colormap (all values mapped to white)
        white_cmap = ListedColormap(["white"])

        # Plot the grid with the white colormap
        _, ax = plt.subplots()
        ax.imshow(np.nan_to_num(self.grid.T, nan=0), cmap=white_cmap)

        # Grid lines
        ax.set_xticks(np.arange(-.5, self.rows, 1), minor=True)
        ax.set_yticks(np.arange(-.5, self.cols, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
        ax.tick_params(which='minor', size=0)
        ax.set_xticks([])
        ax.set_yticks([])

        # Color cells
        for i, j in product(range(self.rows), range(self.cols)):
            val = self.grid[i, j]
            if np.isnan(val):
                ax.add_patch(plt.Rectangle((i - 0.5, j - 0.5), 1, 1, color='black'))
                continue
            
            ax.text(i, j - 0.35, f"V = {self.V[(i, j)]:.3}", va='top', ha='center', fontsize=12, color='black')
            if val > 0:
                ax.add_patch(plt.Rectangle((i - 0.5, j - 0.5), 1, 1, color='#44AA44'))
            elif val < 0:
                ax.add_patch(plt.Rectangle((i - 0.5, j - 0.5), 1, 1, color='#FF4444'))

        for s, a in self.pi.items():
            d = np.array(a) * 0.2
            ax.arrow(s[0] - d[0], s[1] - d[1], d[0], d[1], head_width=0.1, head_length=0.1, fc='black')

        plt.show()