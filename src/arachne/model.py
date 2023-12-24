"""
This file defines directed acyclic hypergraphs, the primary data model used in Arachne, which are used to represent multiple histories of a probabilistic computation. HyperDAGs, unlike their simpler counterpart, directed acyclic graphs, can conveniently preserve ancestry information through branching and merging points by encoding the lineage from a given node to its last unique ancestor in an ordered k-ary relation (a directed hyperedge). In this implementation, nodes are merged when their contents are identical; nodes with only one child are also merged (in a manner reminiscient of a radix trie).

(c) 2023 gaspodethemad
"""

import os

from uuid import uuid4
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple, Union

@dataclass
class Node:
    """Represents a node in a directed hypergraph.
    :param content: Node contents
    :param metadata: Additional information to be stored in the node
    :param ancestry: A list of lists, where each inner list represents a valid ancestry path from this node's parent to last unique ancestor (aka ordered k-ary relation, aka directed hyperedge -- reversed)
    """
    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    ancestry: List[List[str]] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.content)
    
    def __eq__(self, other) -> bool:
        return self.content == other.content and self.ancestry == other.ancestry
    
    
class DirectedHypergraph:
    def __init__(self, create_root=False):
        self.nodes = {}
        if create_root:
            root_node = Node(content=None)
            self.add_node(root_node)
        self.edges = []

    def add_node(self, node: Node) -> str:
        node_id = str(uuid4())
        self.nodes[node_id] = node
        return node_id

    def add_edge(self, edge: List[str]) -> None:
        self.edges.append(edge)
        
        # Add edge segments to node ancestries
        for i in range(1, len(edge)-1):
            self.nodes[edge[i]].ancestry.append(edge[:i][::-1])

        self.nodes[edge[-1]].ancestry.append(edge[:-1][::-1])

    def remove_edge(self, edge: List[str]) -> None:
        if edge in self.edges:
            self.edges.remove(edge)

        # Remove edge segments from node ancestries
        for node_id in edge[1:]:
            if node_id in self.nodes:
                self.nodes[node_id].ancestry = []

    def remove_node(self, node_id: str) -> None:
        if node_id in self.nodes:
            del self.nodes[node_id]

            # Remove edges to and from this node
            edges_to_remove = []
            for edge in self.edges:
                if node_id in edge:
                    edges_to_remove.append(edge)
            for edge in edges_to_remove:
                self.remove_edge(edge)

    def check_for_cycles(self) -> bool:
        for root in self.get_roots():
            if self._check_for_cycles(root, []):
                return True
        return len(self.get_roots()) == 0
    
    def _check_for_cycles(self, node_id: str, visited: List[str]) -> bool:
        if node_id in visited:
            return True 
        visited.append(node_id)
        for child in self.get_children(node_id):
            if self._check_for_cycles(child, visited):
                return True
        return False
    
    def get_nodes(self, node_ids: List[str]) -> List[Node]:
        return [self.nodes[n] for n in node_ids]
    
    def get_node_contents(self, node_ids: List[str]) -> List[Any]:
        return [self.nodes[n].content for n in node_ids]

    def get_roots(self) -> List[str]:
        roots = []
        for node_id in self.nodes:
            if len(self.nodes[node_id].ancestry) == 0:
                roots.append(node_id)
        return roots

    def get_children(self, node_id: str) -> List[str]:
        children = []
        for edge in self.edges:
            if edge[0] == node_id:
                children.append(edge[1])
        return children

    def get_ancestry(self, node_id: str) -> List[List[str]]:
        if node_id in self.get_roots():
            return [[node_id]]
        return [[node_id] + path for path in self._get_ancestries(node_id)]

    def _get_ancestries(self, node_id: str) -> List[List[str]]:
        if self.nodes[node_id].ancestry == []:
            return [[]]

        ancestries = []
        for path in self.nodes[node_id].ancestry:
            for path_ancestry in self._get_ancestries(path[-1]):
                new_ancestry = path.copy()
                new_ancestry.extend(path_ancestry)
                ancestries.append(new_ancestry)
        return ancestries

    def get_node_id(self, node: Node) -> str:
        for node_id, existing_node in self.nodes.items():
            if existing_node == node:
                return node_id
        return None
    
    def refactor(self) -> None:
        """Refactors a hypergraph by merging siblings with identical contents, merging nodes with only one child, and factoring out common contents between nodes into shared parent/child nodes in a fashion reminiscent of a radix trie (but bidirectional)."""
        for root in self.get_roots():
            self._refactor(root)

    def _refactor(self, node_id: str) -> None:
        node = self.nodes[node_id]
        children = self.get_children(node_id)

        # Merge nodes with identical contents
        if len(children) > 0:
            for child in children:
                if self.nodes[child].content == node.content:
                    self.merge([node_id, child])

        # Merge nodes with only one child
        if len(children) == 1:
            child = children[0]
            self.merge([node_id, child])

        # TODO: Factor out common content into shared parent/child nodes
        
        # Recursively refactor children
        for child in self.get_children(node_id):
            self._refactor(child)
            

    def common_ancestor(self, node_ids: List[str]) -> str:
        """Find the last common ancestor between a set of nodes (excluding the nodes themselves)."""
        most_common_ancestors = None
        for node_id in node_ids:
            ancestries = self.get_ancestry(node_id)
            for ancestry in ancestries:
                if most_common_ancestors is None:
                    most_common_ancestors = ancestry
                else:
                    most_common_ancestors = list(set(most_common_ancestors) & set(ancestry))
        most_common_ancestors = sorted(most_common_ancestors, key=lambda x: len(self.nodes[x].ancestry))

        # filter out the nodes themselves
        if most_common_ancestors and len(most_common_ancestors) > 0:
            return list(filter(lambda x: x not in node_ids, most_common_ancestors))[-1]
        else:
            return None
        
    def joint_boundaries(self, node_ids: List[str]) -> Dict[str, Any]:
        """Finds the boundaries between common content in the provided set of nodes, returning a dictionary of node IDs to a list of common content boundaries."""
        raise NotImplementedError("Joint boundary detection must be implemented by a child class.")
        
    def content_lineage(self, content: Any) -> List[str]:
        """Finds the content lineage, the minimal ancestry of nodes whose content is a superset of the provided content object."""
        raise NotImplementedError("Content lineage must be implemented by a child class.")

    def merge(self, node_ids: List[str]) -> str:
        # Implementation for merging nodes in the hypergraph
        raise NotImplementedError("Node merging must be implemented by a child class.")

    def split(self, node_id: str, boundary: Any) -> List[str]:
        # Implementation for splitting nodes in the hypergraph
        raise NotImplementedError("Node splitting must be implemented by a child class.")

    def to_dict(self) -> Dict[str, Any]:
        # Implementation to convert the hypergraph to a dictionary
        raise NotImplementedError("Dictionary conversion must be implemented by a child class.")

    def from_dict(self, state: Dict[str, Any]) -> None:
        # Implementation to create a hypergraph from a dictionary
        raise NotImplementedError("Dictionary conversion must be implemented by a child class.")
    

class StringDirectedHypergraph(DirectedHypergraph):
    def joint_boundaries(self, node_ids: List[str]) -> Dict[str, List[Tuple[int, int]]]:
        """Finds the boundaries between common content in the provided set of nodes, returning a dictionary of node IDs to a list of common content boundaries."""
        node_contents = self.get_node_contents(node_ids)
        boundaries = {}

        """
        TODO: Identify all boundaries of common content for each node in a tuple of (start, end) indices and add them to a dictionary

        Example:
        Node 1 content: "The quick brown fox jumps over the lazy dog."
        Node 2 content: "The quick red car drives over the speedbump.
        Node 3 content: "The quick brown fox jumps over the speedbump."
        Node 4 content: "The quick red car drives over the lazy dog."
        Joint boundaries: {
            node 1: [(0, 10), (24, 35)],
            node 2: [(0, 10), (23, 34)],
            node 3: [(0, 10), (24, 35)],
            node 4: [(0, 10), (23, 34)]
        }
        """

        return boundaries
    
    def content_lineage(self, content: str) -> List[str]:
        """Finds the content lineage, the minimal ancestry of nodes whose content is a superset of the provided content object."""
        for node_id, node in self.nodes.items():
            if content.endswith(node.content):
                ancestries = self.get_ancestry(node_id)
                for ancestry in ancestries:
                    if ''.join(self.get_node_contents(ancestry[::-1])) in content:
                        return ancestry[::-1]
        return []
            
    def merge(self, node_ids: List[str]) -> str:
        # Implementation for merging nodes in the hypergraph
        merged_content = ''.join([self.nodes[node_id].content for node_id in node_ids])
        merged_node = Node(content=merged_content)
        merged_node_id = self.add_node(merged_node)
        for node_id in node_ids:
            self.remove_node(node_id)
        return merged_node_id
        
    def split(self, node_id: str, boundary: Union[List[int], int]) -> List[str]:
        # Implementation for splitting nodes in the hypergraph
        node_content = self.nodes[node_id].content
        if isinstance(boundary, int):
            boundary = [boundary]
        boundary.sort()
        split_nodes = []
        start_index = 0
        for end_index in boundary:
            split_content = node_content[start_index:end_index]
            split_node = Node(content=split_content)
            split_node_id = self.add_node(split_node)
            split_nodes.append(split_node_id)
            start_index = end_index
        split_content = node_content[start_index:]
        split_node = Node(content=split_content)
        split_node_id = self.add_node(split_node)
        split_nodes.append(split_node_id)
        
        # Add edges to the graph to preserve lineage
        ancestries = self.nodes[node_id].ancestry
        if ancestries:
            for ancestry in ancestries:
                # Add edges from the node's parent node to the first split node
                self.add_edge(ancestry[::-1] + [split_nodes[0]])
        for i in range(0, len(split_nodes)-1):
            self.add_edge([split_nodes[i], split_nodes[i+1]])

        # Reparent children of the node to the last split node
        children = self.get_children(node_id)
        for child in children:
            self.add_edge([split_nodes[-1], child])

        # Remove the original node
        self.remove_node(node_id)

        return split_nodes
        
    def to_dict(self) -> Dict[str, Any]:
        # Implementation to convert the hypergraph to a dictionary
        hypergraph_dict = {
            'nodes': {},
            'edges': self.edges
        }
        for node_id, node in self.nodes.items():
            hypergraph_dict['nodes'][node_id] = {
                'content': node.content,
                'metadata': node.metadata,
                'ancestry': node.ancestry
            }
        return hypergraph_dict
        
    def from_dict(self, state: Dict[str, Any]) -> None:
        # Implementation to create a hypergraph from a dictionary
        self.nodes = {}
        self.edges = state['edges']
        for node_id, node_data in state['nodes'].items():
            content = node_data['content']
            metadata = node_data['metadata']
            ancestry = node_data['ancestry']
            node = Node(content=content, metadata=metadata, ancestry=ancestry)
            self.nodes[node_id] = node
