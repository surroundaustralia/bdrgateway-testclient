from typing import Optional

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, VOID

from client._TERN import TERN
from client.model.concept import Concept
from client.model.klass import Klass
from client.model.rdf_dataset import RDFDataset


class FeatureOfInterest(Klass):
    def __init__(
        self, feature_type: Concept, in_dataset: RDFDataset, iri: Optional[str] = None
    ):
        assert (
            type(feature_type) == Concept
        ), "The object supplied for the property feature_type must be of type Concept"

        assert (
            type(in_dataset) == RDFDataset
        ), "The object supplied for the property in_dataset must be of type RDFDataset"

        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/featureofinterest/{self.id}")

        self.iri = URIRef(iri)

        super(FeatureOfInterest, self).__init__(iri)

        self.label = f"Feature of Interest with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"

        self.feature_type = feature_type
        self.in_dataset = in_dataset

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        g.add((self.iri, RDF.type, TERN.FeatureOfInterest))
        g.remove((self.iri, RDFS.label, None))
        g.add((self.iri, RDFS.label, Literal(self.label)))
        g.add((self.iri, TERN.featureType, self.feature_type.iri))
        g.add((self.iri, VOID.inDataset, self.in_dataset.iri))

        return g
