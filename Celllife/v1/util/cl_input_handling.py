__author__ = 'Michael Wagner'

from cab_input_handling import InputHandler


class CellLifeInputHandler(InputHandler):
    def __init__(self, cab_system):
        super().__init__(cab_system)

    def clone(self, cab_sys):
        return InputHandler(cab_sys)
