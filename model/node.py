from model.attributes import Terminal

class Node():
    def __init__(self, id: int, grid_points: list[int], connected_terminals: list[Terminal]):
        self.id = id
        self.grid_points = grid_points
        self.connected_terminals = connected_terminals

    def add_terminal(self, new_terminal: Terminal):
        self.connected_terminals.append(new_terminal)

    def remove_terminal(self, gone_terminal: Terminal):
        self.connected_terminals.remove(gone_terminal)