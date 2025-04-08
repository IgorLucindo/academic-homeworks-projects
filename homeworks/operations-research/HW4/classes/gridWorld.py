import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from itertools import product
import numpy as np


class GridWorld:
    """
    Class for obtaining the optimal policy of the grid world using the policy iteration method
    """
    def __init__(self, grid, flags, gamma=1):
        self.grid = grid
        self.rows, self.cols = grid.shape
        self.plot_flag = flags['plot_iteration']
        self.gamma = gamma

        # Setup
        mask = ~np.isnan(self.grid)
        self.S = [tuple(s) for s in np.array(np.nonzero(mask)).T]
        self.A = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        
        # Initialization
        self.V = {s: 0 for s in self.S}
        self.pi = {s: self.A[0] for s in self.S}


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


    def _next_states(self, s, a):
        """
        Return next possible states given state s and action a
        """
        left = lambda a: [-a[1], a[0]]
        right = lambda a: [a[1], -a[0]]

        # Get possible next states
        sa = np.array(s) + a
        possible_states = [
            tuple(sa + delta)
            for delta in [np.array([0, 0]), left(a), right(a)]
        ]

        # Update possible next states based on wall and grid bound colision
        return self._bounce_back_states(s, possible_states)


    def _P(self, s_prime, next_states):
        """
        Transiction function
        """
        transitions = {
            tuple(next_states[0]): 0.8,
            tuple(next_states[1]): 0.1,
            tuple(next_states[2]): 0.1
        }
        return transitions.get(tuple(s_prime), 0.0)


    def _update_value(self, s, a):
        next_states = self._next_states(s, a)
        return sum(self._P(s_prime, next_states) * (self.grid[s_prime] + self.gamma*self.V[s_prime]) for s_prime in next_states)
        

    def solve_grid_world(self):
        """
        Return optimal policy of grid world obtained by using the policy iteration method
        """
        policy_stable = False
        while True:
            # Show grid on each iteration
            self.show_grid(self.plot_flag)
            
            # Break if policy is stable
            if policy_stable:
                break

            # Policy evaluation
            for s in self.S:
                previous_value = self.V[s]
                self.V[s] = self._update_value(s, self.pi[s])
                print(f"state: {list(s)}   pi: {self.pi[s]}   previous value: {previous_value}   new value: {self.V[s]}")

            # Policy improvement
            policy_stable = True
            for s in self.S:
                previous_pi = self.pi[s]
                action_values = {tuple(a): self._update_value(s, a) for a in self.A}
                self.pi[s] = list(max(action_values, key=action_values.get))
                if previous_pi != self.pi[s]:
                    policy_stable = False


    def show_grid(self, plot_flag):
        """
        Plot grid world
        """
        if not plot_flag: return

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

            if val > 0:
                ax.add_patch(plt.Rectangle((i - 0.5, j - 0.5), 1, 1, color='#44AA44'))
            elif val < 0:
                ax.add_patch(plt.Rectangle((i - 0.5, j - 0.5), 1, 1, color='#FF4444'))

        for s, a in self.pi.items():
            d = np.array(a) * 0.2
            ax.arrow(s[0] - d[0], s[1] - d[1], d[0], d[1], head_width=0.1, head_length=0.1, fc='black')

        plt.title("GridWorld")
        plt.show()