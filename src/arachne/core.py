"""This module provides the Arachne class, which encapsulates the six core operations of the framework: noise, denoise, expand, contract, insert, and delete, which all operate on the contents of nodes in a hypergraph. These are provided as a superclass which is intended to be extended in specific applications of the Arachne framework to specific modalities. Arachne also interfaces with the B'atzb'al package to grow the underlying hypergraph with novel nodes provided by a simulator (a generative model).

(c) 2023 gaspodethemad
"""

from batzbal import Batzbal
from arachne.model import DirectedHypergraph

class Arachne:
    
    def __init__(self, graph: DirectedHypergraph=None):
        self.graph = graph if graph else DirectedHypergraph(create_root=True)
        self.simulator = Batzbal()

    def noise(self, data):
        raise NotImplementedError("The noise operation must be implemented in a concrete Arachne subclass.")

    def denoise(self, data):
        raise NotImplementedError("The denoise operation must be implemented in a concrete Arachne subclass.")

    def expand(self, data):
        raise NotImplementedError("The expand operation must be implemented in a concrete Arachne subclass.")

    def contract(self, data):
        raise NotImplementedError("The contract operation must be implemented in a concrete Arachne subclass.")

    def insert(self, data):
        raise NotImplementedError("The insert operation must be implemented in a concrete Arachne subclass.")

    def delete(self, data):
        raise NotImplementedError("The delete operation must be implemented in a concrete Arachne subclass.")
    
# TODO(gaspode) 2023-12-23: TextArachne (implement noise, denoise, expand, contract, insert, delete on StringDirectedHypergraph) for dealing with strings, using B'atzb'al to interface w/ GPT-4 for text generation