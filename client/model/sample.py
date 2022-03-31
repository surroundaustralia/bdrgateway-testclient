from rdflib import Graph, URIRef, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, VOID
from client.model.klass import Klass
from client._TERN import TERN
from uuid import uuid4
from typing import Optional
from client.model import Concept, RDFDataset


class Sample(Klass):
    def __init__(
        self, in_dataset: RDFDataset, feature_type: Concept, iri: Optional[str] = None
    ):
        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/sample/{self.id}")

        self.iri = URIRef(iri)

        super(Sample, self).__init__(iri)

        self.label = f"Sample with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"

        self.in_dataset = in_dataset.iri
        self.feature_type = feature_type.iri

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        g.add((self.iri, RDF.type, TERN.Sample))
        g.remove((self.iri, RDFS.label, None))
        g.add((self.iri, RDFS.label, Literal(self.label)))
        g.add((self.iri, VOID.inDataset, self.in_dataset))
        g.add((self.iri, TERN.featureType, self.feature_type))

        return g
