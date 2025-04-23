from classes.TicTacToe import *
from utils.solve_utils import *


# Set parameter flags
flags = {
    'plot': True
}


def main():
    # Create Tic-Tac-Toe class
    initial = ('X', 'O', '', '', 'X', '', '', '', 'O')
    tree = TicTacToe(initial, flags)
    tree.plot_decision_tree()

    # Get optimal policy
    pi = get_tic_tac_toe_optimal_policy(tree.boards, tree.successor, tree.remaining_plays, tree.board_result)
    print(f"Best action given initial board: {pi[0]}")


if __name__ == "__main__":
    main()