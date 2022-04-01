from typing import Optional
from uuid import uuid4

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL

from client._TERN import TERN
from client.model.klass import Klass


class RDFDataset(Klass):
    def __init__(self, iri: Optional[str] = None):
        """Receive and use or make an IRI"""
        if iri is None:
            self.id = uuid4()
            iri = URIRef(f"http://example.com/rdfdataset/{self.id}")

        self.iri = URIRef(iri)

        super().__init__(iri)

        self.label = f"RDF Dataset with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        g.add((self.iri, RDF.type, TERN.RDFDataset))
        g.remove((self.iri, RDFS.label, None))
        g.add((self.iri, RDFS.label, Literal(self.label)))

        return g
