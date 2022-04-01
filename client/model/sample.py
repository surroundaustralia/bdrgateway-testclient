from typing import Optional, List, Union

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS, SOSA, VOID

from client._TERN import TERN
from client.model.concept import Concept
from client.model.feature_of_interest import FeatureOfInterest
from client.model.klass import Klass
from client.model.rdf_dataset import RDFDataset


class Sample(Klass):
    def __init__(
        self,
        is_sample_of: List[FeatureOfInterest],
        feature_type: Concept,
        in_dataset: RDFDataset,
        is_result_of: Union["Sampling", None],
        iri: Optional[str] = None,
    ):
        assert (
            len(is_sample_of) >= 1
        ), "You must supply a minimum of 1 FeatureOfInterest objects for the property is_sample_of"

        assert all(
            type(el) == FeatureOfInterest for el in is_sample_of
        ), "Every object supplied in the property is_sample_of must be of type FeatureOfInterest"

        # assert type(is_result_of) == Sampling, \
        #     "The object supplied for the property is_result_of must be of type Sampling"

        assert (
            type(feature_type) == Concept
        ), "The object supplied for the property feature_type must be of type Concept"

        assert (
            type(in_dataset) == RDFDataset
        ), "The object supplied for the property in_dataset must be of type RDFDataset"

        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/sample/{self.id}")

        self.iri = URIRef(iri)

        super(Sample, self).__init__(iri)

        self.label = f"Sample with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"

        self.is_sample_of = is_sample_of
        # self.is_result_of = is_result_of
        self.feature_type = feature_type
        self.in_dataset = in_dataset

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        g.add((self.iri, RDF.type, TERN.Sample))
        g.remove((self.iri, RDFS.label, None))
        g.add((self.iri, RDFS.label, Literal(self.label)))
        for iso in self.is_sample_of:
            g.add((self.iri, SOSA.isSampleOf, iso.iri))
        # g.add((self.iri, SOSA.isResultOf, self.is_result_of.iri))
        g.add((self.iri, TERN.featureType, self.feature_type.iri))
        g.add((self.iri, VOID.inDataset, self.in_dataset.iri))

        return g
