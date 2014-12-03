"""
Main module of the Flow and Pressure Demo.
Uses the Complex Automaton Base.
"""

from cab_system import ComplexAutomaton

from v1.global_constants import CellLifeGC
from v1.ca.cl_cell import CellLifeCell
from v1.abm.cl_agent import CellLifeSpawner
from v1.util.cl_input_handling import CellLifeInputHandler
from v1.util.cl_visualization import CellLifeVisualizer


__author__ = 'Michael Wagner'


if __name__ == '__main__':
    gc = CellLifeGC()
    pc = CellLifeCell(0, 0, 0, gc)
    pa = CellLifeSpawner(-1, -1, gc)
    ph = CellLifeInputHandler(None)
    pv = CellLifeVisualizer(gc, None)
    simulation = ComplexAutomaton(gc, proto_cell=pc, proto_agent=pa, proto_handler=ph, proto_visualizer=pv)
    simulation.run_main_loop()