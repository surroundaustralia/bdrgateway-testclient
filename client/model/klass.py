from typing import Optional
from uuid import uuid4

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL

from client.model._TERN import TERN


class Klass:
    iri = None

    def __init__(self, iri: Optional[str] = None):
        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/{self.id}")

        self.iri = URIRef(iri)
        self.label = f"Class with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"

    def make_uuid(self):
        return uuid4()

    def to_graph(self) -> Graph:
        g = Graph()
        g.bind("tern", TERN)

        g.add((self.iri, RDF.type, OWL.Class))
        g.add((self.iri, RDFS.label, Literal(self.label)))

        return g
