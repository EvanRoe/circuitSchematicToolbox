from controller.commands import Command

class CommandStack:
    def execute(self, command: Command) -> None:
        ...

    def undo(self) -> None:
        ...

    def redo(self) -> None:
        ...