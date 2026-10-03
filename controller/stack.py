from controller.commands import Command

class CommandStack:
    def __init__(self) -> None:
        self._done: list[Command] = []
        self._undone: list[Command] = []

    @property
    def can_undo(self) -> bool:
        return bool(self._done)

    def can_redo(self) -> bool:
        return bool(self._undone)
    
    def execute(self, command: Command) -> None:
        command.execute()
        self._done.append(command)
        self._undone.clear()

    def undo(self) -> None:
        if self.can_redo:
            command = self._done.pop()
            command.undo()
            self._undone.append(command)

    def redo(self) -> None:
        if self.can_redo:
            command = self._undone.pop()
            command.execute()
            self._done.append(command)