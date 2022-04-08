from typing import Optional

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS

from client.model.klass import Klass


class Concept(Klass):
    def __init__(self, iri: Optional[str] = None, pref_label: Optional[str] = None):
        if pref_label is not None:
            assert isinstance(pref_label.__class__, str.__class__), \
                "If you provide a value for the prefLabel parameter, it must be of type string"

        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/concept/{self.id}")

        self.iri = URIRef(iri)

        super(Concept, self).__init__(iri)

        if pref_label is not None:
            self.pref_label = pref_label
            self.label = pref_label
        else:
            self.pref_label = f"RDF Dataset with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"
            self.label = self.pref_label

        self.label = f"Concept with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        g.add((self.iri, RDF.type, SKOS.Concept))
        g.remove((self.iri, RDFS.label, None))
        g.add((self.iri, RDFS.label, Literal(self.label)))

        if hasattr(self, "title"):
            g.add((self.iri, SKOS.prefLabel, Literal(self.title, lang="en")))

        return g
