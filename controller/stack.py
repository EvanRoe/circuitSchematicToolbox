"""
@file stack.py
@brief Holds the command stack.
@author Evan Roe
@date 2026-10-03
"""
from controller.commands import Command

class CommandStack:
    """Represents the command stack to be able to manipulate actioned commands."""
    def __init__(self) -> None:
        """Constructs a CommandStack, making done and undone lists as the command stacks."""
        self._done: list[Command] = []
        self._undone: list[Command] = []

    @property
    def can_undo(self) -> bool:
        """Property function on whether the done list is empty or not."""
        return bool(self._done)

    @property
    def can_redo(self) -> bool:
        """Property function on whether the undone list is empty or not."""
        return bool(self._undone)
    
    def execute(self, command: Command) -> None:
        """Runs the execute method on the command and updates the stack."""
        command.execute()
        self._done.append(command)
        self._undone.clear()

    def undo(self) -> None:
        """Runs the undo method and updates the stack."""
        if self.can_undo:
            command = self._done.pop()
            command.undo()
            self._undone.append(command)

    def redo(self) -> None:
        """Redoes the last undone command and updates the stack."""
        if self.can_redo:
            command = self._undone.pop()
            command.execute()
            self._done.append(command)