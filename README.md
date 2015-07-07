Cellular-Automata
=================
This repository contains a collection of simple simulations based on cellular automata (CA):
* **LatticeGasCA**
  * A very simplistic model of gas particle movement, using the Margolus-neighborhood
* **ThermalCreep**
  * A simple model of certain fictitious substances (creep) being propagated though a grid, by agents
  * The exact purpose of this sub-project is not determined yet, it might either lead to aquarium-like artificial life simulations or games.
  * Inspired by games like Starcraft and Creeper World 3.
  * It is intended to integrate physical or pseudo-physical aspects into the simulations, e.g.: temperature.
* **Sugarscape**
  * Artificial Life simulation, first conceived by Axtell and Epstein. [Wikipedia](http://en.wikipedia.org/wiki/Sugarscape)
  * It consists of agents who move through an artificial world laid out as a grid and try to survive by harvesting resources (sugar and spice). All the while they are trying to sustain their needs by either foraging or trading. Agents also have to procreate and fight diseases and competitors from other tribes. The most interesting aspect to Sugarscape is to create emergent behavior while trying to keep the agents' behavioral rules as simple as possible.
  * **V0**
    * A very basic implementation: only one resource, agents forage and influence others culture.
    * no longer in development
  * **V1**
    * More advanced version: two resources, tribes and trading, reproduction.
    * no longer in development
  * **V2**
    * Most advanced version so far. Code has been cleaned up a lot compared to V1.
    * Features: two resources, harvesting, trading, tribes, territoriality, combat, reproduction, diseases, mendelian genetics etc.

**Technical Requirements**

All of the sub-projects are written completely in Python 3.4 and use the Pygame engine for visualization.
Required libraries are:
* Matplotlib
* Numpy
* Pygame

all of which can be found here: http://www.lfd.uci.edu/~gohlke/pythonlibs/ (windows only)

**Media**

This [short clip](http://www.youtube.com/watch?v=930o5KScl-o) shows the Sugarscape V2 in action.
