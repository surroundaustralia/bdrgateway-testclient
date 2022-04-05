from typing import Optional
from uuid import uuid4

from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS

from client.model._TERN import TERN
from client.model.klass import Klass


class Value(Klass):
    def __init__(
            self,
            is_blank_node: Optional[bool] = True,
            iri: Optional[str] = None
    ):
        if is_blank_node:
            assert iri is None, \
                "If you set this Value to be a Blank Node (is_blank_node == True) then you cannot allocate it an IRI"

        self.is_blank_node = is_blank_node

        if self.is_blank_node:
            self.iri = BNode()
            self.label = "Value Blank Node"
        else:
            """Receive and use or make an IRI"""
            if iri is None:
                self.id = uuid4()
                iri = URIRef(f"http://example.com/value/{self.id}")

            self.iri = URIRef(iri)
            super().__init__(iri)
            self.label = f"Value with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"

    def to_graph(self) -> Graph:
        g = Graph()
        g.bind("tern", TERN)
        g.add((self.iri, RDF.type, TERN.Value))
        g.add((self.iri, RDFS.label, Literal(self.label)))

        return g
