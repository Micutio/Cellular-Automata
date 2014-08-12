Cellular-Automata
=================
This repository contains a collection of simple simulations based on cellular automatons (CA):
* **LatticeGasCA**
  * A very simplistic model of gas particle movement.
  * V2 is only slightly more advanced using the margolus neighborhood
  * currently not in development
* **ThermalCreep**
  * A simple model of certain substances (creep) being propagated though a grid, either by themselves (v1) or agents (v2).
  * The exact purpose of this subproject is not determined yet, it might either lead to aquarium-like artificial life simulations or games.
  * Inspired by games like Starcraft and Creeper World 3.
  * The term "thermal" denotes the intention to integrate physical or pseudo-physical aspects into the simulations, e.g.: temperature.
  * development currently paused
* **Sugarscape**
  * Artificial Life simulation, first conceived by Axtell and Epstein. [Wikipedia](http://en.wikipedia.org/wiki/Sugarscape)
  * It consists of agents who move across an artificial world based on a CA and try to survive by harvesting resources. The most interesting part is to create emergent behavior while trying to keep the agents' behavioral rules as simple as possible.
  * **V0**
    * Simplest possible implementation: only one resource, agents gather and influence others culture.
    * no longer in development
  * **V1**
    * More advanced version: two resources, tribes and trading, reproduction.
    * no longer in development
  * **V2**
    * Most dvanced version so far. Code has been cleaned up a lot compared to V1.
    * Features: two resources, harvesting, trading, tribes, territoriality, combat, reproduction, diseases, mendelian genetics etc.
    * **currently in development**

**Technical Requirements**
All of the subprojects are written completely in Python 3.4 and use the pygame engine for visualization.
Required libraries are:
* matplotlib
* numpy
* pygame

all of which can be found here: http://www.lfd.uci.edu/~gohlke/pythonlibs/ (windows only)
