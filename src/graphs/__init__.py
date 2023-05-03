import os
import contextvars
import uuid
from pathlib import Path
from typing import List, Union, Dict
from graphviz import Digraph

graph_instance = contextvars.ContextVar("")


def get_graph() -> "Graph":
    return graph_instance.get()

def set_graph(graph: "Graph"):
    graph_instance.set(graph)

class Graph:
    graph_attrs = {
        "pad": "1.0",
        "splines": "ortho",
        "nodesep": "0.60",
        "ranksep": "0.75",
        "fontname": "Sans-Serif",
        "fontsize": "13",
        "fontcolor": "#2D3436",
    }
    node_attrs = {
        "shape": "box",
        "style": "rounded",
        "width": "1.4",
        "height": "1.4",
        "labelloc": "b",
        "imagescale": "true",
        "fontname": "Sans-Serif",
        "fontsize": "13",
        "fontcolor": "#2D3436",
    }
    edge_attrs = {
        "color": "#7B8894",
    }
    _carbon_emission=0
    def __init__(
        self,
        name: str = "",
        filename: str = "",
        function_unit: str ="",
        function_count: int =0,
        start_period: str ="",
        end_period:str = ""
    ):
        self.name = name
        self.filename = filename
        self.dot = Digraph(self.name, filename=self.filename)
        self.function_unit = function_unit
        self.function_count = function_count
        self.start_period = start_period
        self.end_period = end_period
        self.dot.graph_attr["label"] = self.name
        self.outformat = "png"

        # Merge passed in attributes
        self.dot.graph_attr.update(self.graph_attrs)
        self.dot.node_attr.update(self.node_attrs)
        self.dot.edge_attr.update(self.edge_attrs)

        self.show = False

    def __str__(self) -> str:
        return str(self.dot)

    def __enter__(self):
        set_graph(self)
        return self

    def __exit__(self,error_instance,error,traceback):
        node_attr={
            'height':"1.2",
            'width':"2.0",
            'shape':'box',
            'labelloc':"c",
            "fontname": "Sans-Serif",
            "fontsize": "15",
            "fontcolor": "#2D3436",
        }
        self.dot.node("function",self.function_unit + " = " + str(self.function_count),**node_attr)
        sci_score = self._carbon_emission/self.function_count
        self.dot.node("emission","SCI Score \n= " + str(round(sci_score,3))+" KgCo2eq",**node_attr)
        self.dot.node("start_period","Start Period \n= " + self.start_period,**node_attr)
        self.dot.node("end_period","End Period \n= " + self.end_period,**node_attr)
        
        self.render()
        os.remove(self.filename)
        set_graph(None)

    def node(self, nodeid: str, label: str, **attrs) -> None:
        self.dot.node(nodeid, label=label, **attrs)

    def connect(self, node: "Node", node2: "Node", edge: "Edge") -> None:
        self.dot.edge(node.nodeid, node2.nodeid, **edge.attrs)

    def subgraph(self, dot: Digraph) -> None:
        self.dot.subgraph(dot)

    def render(self) -> None:
        self.dot.render(format=self.outformat, view=self.show, quiet=True)


class Node:
    """Node represents a node for a  software boundry in ontology."""

    ontology_type=None

    image_dir = None
    image_name = None
    label = None

    height = 1.9

    def __init__(self, label: str = "", **attrs: Dict):
        """Node represents a software boundry component.

        :param label: Node label.
        """
        # Generates an ID for identifying a node
        self.nodeid = uuid.uuid4().hex
        self.label = label

        self.graph = get_graph()

        self.node_attrs = {
            "shape": "none",
            "height": str(self.height),
            "image": self.load_image(),
        }

        self.node_attrs.update(attrs)

        self.graph.node(self.nodeid, self.label, **self.node_attrs)

    
    def undirected_edge(self, other: Union["Node", List["Node"]]):
        if isinstance(other, list):
            for node in other:
                self.connect(node, Edge(self))
            return other
        elif isinstance(other, Node):
            return self.connect(other, Edge(self))
        else:
            other.node = self
            return other
        
    def forward_edge(self, other: Union["Node", List["Node"]]):
        if isinstance(other, list):
            for node in other:
                self.connect(node, Edge(self, forward=True))
            return other
        else:
            return self.connect(other, Edge(self, forward=True))

    def backward_edge(self, other: Union["Node", List["Node"]]):
        if isinstance(other, list):
            for node in other:
                self.connect(node, Edge(self, reverse=True))
            return other
        else:
            return self.connect(other, Edge(self, reverse=True))

    def connect(self, node: "Node", edge: "Edge"):
        self.graph.connect(self, node, edge)
        return node

    def load_image(self):
        basedir = Path(os.path.abspath(os.path.dirname(__file__)))
        return os.path.join(basedir.parent, self.image_dir, self.image_name)


class Edge:
    """Edge represents an edge between two nodes."""

    edge_attrs = {
        "fontcolor": "#2D3436",
        "fontname": "Sans-Serif",
        "fontsize": "13",
    }

    def __init__(
        self,
        node: "Node" = None,
        forward: bool = False,
        reverse: bool = False,
        **attrs: Dict,
    ):

        self.node = node
        self.forward = forward
        self.reverse = reverse

        self.edge_attrs.update(attrs)

    @property
    def attrs(self) -> Dict:
        if self.forward and self.reverse:
            direction = "both"
        elif self.forward:
            direction = "forward"
        elif self.reverse:
            direction = "back"
        else:
            direction = "none"
        return {**self.edge_attrs, "dir": direction}

