import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class TicTacToe():
    """
    Class for creating a decision tree for Tic-Tac-Toe
    """
    def __init__(self, initial_board, flags):
        # Initial board should be tuple
        self.boards = [{initial_board}]
        self.flags = flags
        
        self.remaining_plays = initial_board.count('')
        self.first_player = 'X' if self.remaining_plays % 2 == 1 else 'O'
        self.player = self.first_player
        self.successor = {}
        self.board_result = {}

        # Set boards
        self.set_boards()


    def set_boards(self):
        """
        Create boards for decision tree
        """
        for i in range(self.remaining_plays):
            self._set_layer_boards(i)
            self._toggle_player()
        
        # Set draw results
        for b in self.boards[-1]:
            self.board_result[b] = 0

            
    def _set_layer_boards(self, layer):
        """
        Get possible boards of a layer in the decision tree
        """
        next_layer_boards = set()

        # Get next boards
        for b in self.boards[layer]:
            # Check if game ended
            terminated, result = self._is_terminal(b)
            if terminated:
                self.successor[b] = set()
                self.board_result[b] = result
                continue

            possible_boards = self._next_boards(b)
            canonical_successors = {self._get_canonical(b2) for b2 in possible_boards}

            self.successor[b] = canonical_successors
            next_layer_boards.update(canonical_successors)

        # Append next layer boards
        self.boards.append(next_layer_boards)


    def _next_boards(self, b):
        """
        Generate all possible plays for a given board
        """
        possible_boards = set()
        
        # Iterate over the board and find empty spots
        for i in range(9):
            if b[i] == '':
                new_board = list(b)
                new_board[i] = self.player
                possible_boards.add(tuple(new_board))
        
        return possible_boards
    

    def _is_terminal(self, b):
        """
        Check if the game is over (win or draw)
        """
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]

        for i, j, k in lines:
            if b[i] != '' and b[i] == b[j] == b[k]:
                return True, 1 if b[i] == self.first_player else -1  # Win detected

        return False, 0  # Game is still going
    

    def _get_canonical(self, b):
        """
        Returns the canonical (lex smallest) version of the board
        """
        return min(self._get_symmetries(b))
    

    def _get_symmetries(self, b):
        """
        Returns all 8 symmetries of a 3x3 board (rotations and reflections)
        """
        def rotate(b): return (b[6], b[3], b[0], b[7], b[4], b[1], b[8], b[5], b[2])
        def reflect(b): return (b[2], b[1], b[0], b[5], b[4], b[3], b[8], b[7], b[6])

        boards = []
        current = b
        for _ in range(4):
            boards.append(current)
            boards.append(reflect(current))
            current = rotate(current)

        return boards
    

    def _toggle_player(self):
        self.player = 'X' if self.player == 'O' else 'O'

    
    def plot_decision_tree(self, figsize=(14, 8)):
        """
        Plot the decision tree using networkx and matplotlib with layers aligned,
        based on the number of remaining plays plus one, and centralized vertices.
        """
        if not self.flags['plot']:
            return

        G = nx.DiGraph()

        # Board label
        def board_to_str(board):
            lines = []
            for i in range(0, 9, 3):
                row = ' | '.join(f"{cell or ' ':^1}" for cell in board[i:i+3])
                lines.append(f" {row} ")
                if i < 6:
                    lines.append("-----------")
            return '\n'.join(lines)

        pos = {}
        labels = {}
        node_x_offsets = {}

        max_depth = self.remaining_plays + 1
        spacing_factor = 4  # Controls horizontal and vertical spacing

        for layer, boards in enumerate(self.boards[:max_depth]):
            node_x_offsets[layer] = 0
            num_boards = len(boards)
            center_x = (num_boards - 1) / 2
            for idx, board in enumerate(boards):
                board_str = board_to_str(board)
                if board_str not in pos:
                    x = (idx - center_x) * spacing_factor
                    y = -layer * spacing_factor
                    pos[board_str] = (x, y)
                    labels[board_str] = board_str
                G.add_node(board_str)

        for layer, boards in enumerate(self.boards[:max_depth]):
            for board in boards:
                parent_str = board_to_str(board)
                for succ in self.successor.get(board, []):
                    succ_str = board_to_str(succ)

                    if succ_str not in pos and layer + 1 < max_depth:
                        num_succ = len(self.successor.get(board, []))
                        center_x = (num_succ - 1) / 2
                        x = (node_x_offsets[layer + 1] - center_x) * spacing_factor
                        y = -(layer + 1) * spacing_factor
                        pos[succ_str] = (x, y)
                        labels[succ_str] = succ_str
                        node_x_offsets[layer + 1] += 1

                    G.add_edge(parent_str, succ_str)

        plt.figure(figsize=figsize)
        
        # Only draw edges (we'll draw custom square nodes)
        nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=5)

        # Draw square nodes manually
        ax = plt.gca()
        node_width = 3.5  # Width of square node (adjust as needed)
        node_height = 1.2  # Height of square node

        for i, (node, (x, y)) in enumerate(pos.items()):
            # Draw a light blue square
            square = patches.FancyBboxPatch(
                (x - node_width / 2, y - node_height / 2),
                node_width, node_height,
                boxstyle="round,pad=0.02",  # Use "square" if no rounded corners
                linewidth=1,
                facecolor="white",
                edgecolor="black"
            )
            ax.add_patch(square)
        
        for node, (x, y) in pos.items():
            plt.text(
                x, y, labels[node],
                fontsize=6, ha='center', va='center',
                family='monospace'
            )


        plt.title("Tic-Tac-Toe Decision Tree (Layered, Centralized)", fontsize=14)
        plt.axis('off')
        plt.tight_layout()
        plt.show()