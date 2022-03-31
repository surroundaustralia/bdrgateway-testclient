from rdflib import Graph, URIRef, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS
from client.model.klass import Klass
from typing import Optional


class Concept(Klass):
    def __init__(self, iri: Optional[str] = None):
        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/concept/{self.id}")

        self.iri = URIRef(iri)

        super(Concept, self).__init__(iri)

        self.label = f"Concept with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        g.add((self.iri, RDF.type, SKOS.Concept))
        g.remove((self.iri, RDFS.label, None))
        g.add((self.iri, RDFS.label, Literal(self.label)))

        return g
