import pytest
from arachne.model import DirectedHypergraph, Node, StringDirectedHypergraph

@pytest.fixture
def graph():
    return DirectedHypergraph()

def test_add_node(graph):
    node = Node("A")
    node_id = graph.add_node(node)
    assert node_id in graph.nodes
    assert graph.nodes[node_id] == node

def test_add_edge(graph):
    node1 = Node("A")
    node2 = Node("B")
    node1_id = graph.add_node(node1)
    node2_id = graph.add_node(node2)
    edge = [node1_id, node2_id]
    graph.add_edge(edge)
    assert edge in graph.edges
    assert node2.ancestry == [[node1_id]]

def test_remove_edge(graph):
    node1 = Node("A")
    node2 = Node("B")
    node1_id = graph.add_node(node1)
    node2_id = graph.add_node(node2)
    edge = [node1_id, node2_id]
    graph.add_edge(edge)
    graph.remove_edge(edge)
    assert edge not in graph.edges
    assert node2.ancestry == []

def test_remove_node(graph):
    node = Node("A")
    node_id = graph.add_node(node)
    graph.remove_node(node_id)
    assert node_id not in graph.nodes

def test_check_for_cycles(graph):
    node1 = Node("A")
    node2 = Node("B")
    node3 = Node("C")
    node1_id = graph.add_node(node1)
    node2_id = graph.add_node(node2)
    node3_id = graph.add_node(node3)
    graph.add_edge([node1_id, node2_id])
    graph.add_edge([node2_id, node3_id])
    graph.add_edge([node3_id, node1_id])
    assert graph.check_for_cycles()

def test_get_roots(graph):
    node1 = Node("A")
    node2 = Node("B")
    node3 = Node("C")
    node1_id = graph.add_node(node1)
    node2_id = graph.add_node(node2)
    node3_id = graph.add_node(node3)
    graph.add_edge([node1_id, node2_id])
    graph.add_edge([node1_id, node3_id])
    assert graph.get_roots() == [node1_id]

def test_get_children(graph):
    node1 = Node("A")
    node2 = Node("B")
    node3 = Node("C")
    node1_id = graph.add_node(node1)
    node2_id = graph.add_node(node2)
    node3_id = graph.add_node(node3)
    graph.add_edge([node1_id, node2_id])
    graph.add_edge([node1_id, node3_id])
    assert graph.get_children(node1_id) == [node2_id, node3_id]

def test_get_ancestry(graph):
    node1 = Node("A")
    node2 = Node("B")
    node3 = Node("C")
    node4 = Node("D")
    node5 = Node("E")
    node6 = Node("F")
    
    node1_id = graph.add_node(node1)
    node2_id = graph.add_node(node2)
    node3_id = graph.add_node(node3)
    node4_id = graph.add_node(node4)
    node5_id = graph.add_node(node5)
    node6_id = graph.add_node(node6)
    
    graph.add_edge([node1_id, node2_id])
    graph.add_edge([node1_id, node3_id])
    graph.add_edge([node2_id, node4_id])
    graph.add_edge([node2_id, node5_id])
    graph.add_edge([node3_id, node4_id])
    graph.add_edge([node4_id, node6_id])
    graph.add_edge([node5_id, node6_id])
    
    assert graph.get_ancestry(node1_id) == [[node1_id]]
    assert graph.get_ancestry(node2_id) == [[node2_id, node1_id]]
    assert graph.get_ancestry(node3_id) == [[node3_id, node1_id]]
    assert graph.get_ancestry(node4_id) == [[node4_id, node2_id, node1_id], [node4_id, node3_id, node1_id]]
    assert graph.get_ancestry(node5_id) == [[node5_id, node2_id, node1_id]]
    assert graph.get_ancestry(node6_id) == [[node6_id, node4_id, node2_id, node1_id], [node6_id, node4_id, node3_id, node1_id], [node6_id, node5_id, node2_id, node1_id]]

def test_node_ancestry(graph):
    node1 = Node("A")
    node2 = Node("B")
    node3 = Node("C")
    node4 = Node("D")
    node5 = Node("E")
    node6 = Node("F")
    node7 = Node("G")
    node8 = Node("H")
    node9 = Node("I")
    node10 = Node("J")
    
    node1_id = graph.add_node(node1)
    node2_id = graph.add_node(node2)
    node3_id = graph.add_node(node3)
    node4_id = graph.add_node(node4)
    node5_id = graph.add_node(node5)
    node6_id = graph.add_node(node6)
    node7_id = graph.add_node(node7)
    node8_id = graph.add_node(node8)
    node9_id = graph.add_node(node9)
    node10_id = graph.add_node(node10)
    
    # Add hyperedges
    hyperedge1 = [node1_id, node2_id, node3_id]
    hyperedge2 = [node2_id, node4_id, node5_id]
    hyperedge3 = [node3_id, node6_id, node7_id]
    hyperedge4 = [node4_id, node8_id, node9_id]
    hyperedge5 = [node5_id, node10_id]
    hyperedge6 = [node4_id, node10_id]
    
    graph.add_edge(hyperedge1)
    graph.add_edge(hyperedge2)
    graph.add_edge(hyperedge3)
    graph.add_edge(hyperedge4)
    graph.add_edge(hyperedge5)
    graph.add_edge(hyperedge6)
    
    assert node10.ancestry == [[node5_id], [node4_id]]
    assert node9.ancestry == [[node8_id, node4_id]]
    assert node8.ancestry == [[node4_id]]
    assert node7.ancestry == [[node6_id, node3_id]]
    assert node6.ancestry == [[node3_id]]
    assert node5.ancestry == [[node4_id, node2_id]]
    assert node4.ancestry == [[node2_id]]
    assert node3.ancestry == [[node2_id, node1_id]]
    assert node2.ancestry == [[node1_id]]
    assert node1.ancestry == []

def test_get_node_id(graph):
    node1 = Node("A")
    node2 = Node("B")
    node1_id = graph.add_node(node1)
    node2_id = graph.add_node(node2)
    assert graph.get_node_id(node1) == node1_id
    assert graph.get_node_id(node2) == node2_id
    
def test_common_ancestor(graph):
    node1 = Node("A")
    node2 = Node("B")
    node3 = Node("C")
    node4 = Node("D")
    node5 = Node("E")
    node6 = Node("F")
    node1_id = graph.add_node(node1)
    node2_id = graph.add_node(node2)
    node3_id = graph.add_node(node3)
    node4_id = graph.add_node(node4)
    node5_id = graph.add_node(node5)
    node6_id = graph.add_node(node6)
    graph.add_edge([node1_id, node2_id])
    graph.add_edge([node1_id, node3_id])
    graph.add_edge([node2_id, node4_id])
    graph.add_edge([node2_id, node5_id])
    graph.add_edge([node5_id, node6_id])
    assert graph.common_ancestor([node4_id, node5_id]) == node2_id
    assert graph.common_ancestor([node2_id, node3_id]) == node1_id
    assert graph.common_ancestor([node5_id, node6_id]) == node2_id

@pytest.fixture
def graph():
    return StringDirectedHypergraph()

def test_merge(graph):
    node1 = Node("Hello ")
    node2 = Node("World!")
    node1_id = graph.add_node(node1)
    node2_id = graph.add_node(node2)
    merged_node_id = graph.merge([node1_id, node2_id])
    assert merged_node_id in graph.nodes
    assert graph.nodes[merged_node_id].content == "Hello World!"
    assert node1_id not in graph.nodes
    assert node2_id not in graph.nodes

def test_split(graph):
    node = Node("Hello World!")
    node_id = graph.add_node(node)
    split_node_ids = graph.split(node_id, 6)
    assert len(split_node_ids) == 2
    assert split_node_ids[0] in graph.nodes
    assert split_node_ids[1] in graph.nodes
    assert graph.nodes[split_node_ids[0]].content == "Hello "
    assert graph.nodes[split_node_ids[1]].content == "World!"
    assert node_id not in graph.nodes
    assert sorted(graph.edges) == [[split_node_ids[0], split_node_ids[1]]]

def test_to_dict(graph):
    node1 = Node("Hello ")
    node2 = Node("World!")
    node1_id = graph.add_node(node1)
    node2_id = graph.add_node(node2)
    graph.add_edge([node1_id, node2_id])
    hypergraph_dict = graph.to_dict()
    assert 'nodes' in hypergraph_dict
    assert 'edges' in hypergraph_dict
    assert node1_id in hypergraph_dict['nodes']
    assert node2_id in hypergraph_dict['nodes']
    assert hypergraph_dict['edges'] == [[node1_id, node2_id]]

def test_from_dict(graph):
    hypergraph_dict = {
        'nodes': {
            'node1': {
                'content': 'Hello ',
                'metadata': {},
                'ancestry': []
            },
            'node2': {
                'content': 'World!',
                'metadata': {},
                'ancestry': [
                    'node1'
                ]
            }
        },
        'edges': [['node1', 'node2']]
    }
    graph.from_dict(hypergraph_dict)
    assert 'node1' in graph.nodes
    assert 'node2' in graph.nodes
    assert graph.nodes['node1'].content == 'Hello '
    assert graph.nodes['node2'].content == 'World!'
    assert graph.edges == [['node1', 'node2']]
    
def test_content_lineage(graph):
    node1 = Node("The quick ")
    node2 = Node("brown fox jumps ")
    node3 = Node("red car drives ")
    node4 = Node("over the ")
    node5 = Node("lazy dog.")
    node6 = Node("speedbump.")
    node1_id = graph.add_node(node1)
    node2_id = graph.add_node(node2)
    node3_id = graph.add_node(node3)
    node4_id = graph.add_node(node4)
    node5_id = graph.add_node(node5)
    node6_id = graph.add_node(node6)
    graph.add_edge([node1_id, node2_id, node4_id])
    graph.add_edge([node1_id, node3_id, node4_id])
    graph.add_edge([node2_id, node4_id, node5_id])
    graph.add_edge([node3_id, node4_id, node6_id])
    
    assert graph.content_lineage("The quick brown fox jumps over the lazy dog.") == [node1_id, node2_id, node4_id, node5_id]
    assert graph.content_lineage("The quick red car drives over the speedbump.") == [node1_id, node3_id, node4_id, node6_id]

def test_joint_boundaries(graph):
    node1 = Node("The quick brown fox jumps over the lazy dog.")
    node2 = Node("The quick red car drives over the speedbump.")
    node3 = Node("The quick brown fox jumps over the speedbump.")
    node4 = Node("The quick red car drives over the lazy dog.")
    node1_id = graph.add_node(node1)
    node2_id = graph.add_node(node2)
    node3_id = graph.add_node(node3)
    node4_id = graph.add_node(node4)
    boundaries = graph.joint_boundaries([node1_id, node2_id, node3_id, node4_id])
    assert boundaries == {node1_id: [(0, 10), (24, 35)], node2_id: [(0, 10), (23, 34)], node3_id: [(0, 10), (24, 35)], node4_id: [(0, 10), (23, 34)]}