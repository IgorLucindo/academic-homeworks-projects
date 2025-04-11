from classes.TicTacToe import *


# Set parameter flags
flags = {
    'plot': True
}


def main():
    # Create Tic-Tac-Toe class
    initial = ('X', 'O', '', '', 'X', '', '', '', 'O')
    tree = TicTacToe(initial, flags)
    tree.plot_decision_tree()


if __name__ == "__main__":
    main()