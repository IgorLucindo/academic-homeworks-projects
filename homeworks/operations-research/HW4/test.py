# Board label
def board_to_str(board, padding=2):
    lines = []
    space = " " * padding
    for i in range(0, 9, 3):
        row_cells = board[i:i+3]
        formatted_cells = [f"{cell or ' ':^{3 + 2 * padding}}" for cell in row_cells]
        row = ' | '.join(formatted_cells)
        lines.append(f"{space}{row}{space}")
        if i < 6:
            lines.append(f"{space}{'-' * (11 + 6 * padding)}{space}")
    return '\n'.join(lines)

# Example usage:
board1 = [1, 2, 3, None, 5, None, 7, 8, 9]
print(board_to_str(board1))

print("\nWith more padding:")
board2 = [1, 2, 3, None, 5, None, 7, 8, 9]
print(board_to_str(board2, padding=4))