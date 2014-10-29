"""
Exemplary main module of the Complex Automaton Base.
"""

from cab_global_constants import GlobalConstants
from cab_system import ComplexAutomaton

__author__ = 'Michael Wagner'

if __name__ == '__main__':
    GC = GlobalConstants()
    simulation = ComplexAutomaton(GC,
                                  proto_cell=None,
                                  proto_agent=None,
                                  proto_handler=None,
                                  proto_visualizer=None)
    simulation.run_main_loop()