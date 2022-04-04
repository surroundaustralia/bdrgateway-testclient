from typing import Optional, Union, List

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, VOID, SOSA

from client._TERN import TERN
from client.model import Sample
from client.model.concept import Concept
from client.model.klass import Klass
from client.model.rdf_dataset import RDFDataset
from client.model.feature_of_interest import FeatureOfInterest


class Site(Klass):
    def __init__(
        self,
            is_result_of: Union["Sample", None],
            is_sample_of: List[FeatureOfInterest],
            in_dataset: RDFDataset,
            label: Literal,
            feature_type: Concept,
            iri: Optional[str] = None
    ):
        # assert (
        #     len(is_result_of) == 0
        # ), "You must supply a minimum of 1 sosa:isResultOf Samplings"

        assert (
            len(is_sample_of) >= 1
        ), "You must supply a minimum of 1 Sample object(s)" \
           " for the property is_sample_of"

        assert (
            type(feature_type) == Concept
        ), "The object supplied for the property feature_type must be of type Concept"

        assert (
            type(in_dataset) == RDFDataset
        ), "The object supplied for the property in_dataset must be of type RDFDataset"

        # this is potentially problematic as these sites shouldn't be random
        # But for now will continue and use the same logic as prior
        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/site/{self.id}")

        self.iri = URIRef(iri)
        super().__init__(iri)
        self.label = label
        self.feature_type = feature_type
        self.in_dataset = in_dataset
        self.is_result_of = is_result_of
        self.is_sample_of = is_sample_of
    #

    def to_graph(self) -> Graph:
        g = super().to_graph()
        # removing Klass.py graph structures
        g.remove((self.iri, RDF.type, OWL.Class))
        g.remove((self.iri, RDFS.label, None))
        # overwriting/adding the klass.py

        g.add((self.iri, RDF.type, TERN.Site))
        g.add((self.iri, RDFS.label, Literal(self.label)))
        g.add((self.iri, TERN.featureType, self.feature_type.iri))
        g.add((self.iri, VOID.inDataset, self.in_dataset.iri))

        if self.is_result_of is not None:
            g.add((self.iri, SOSA.isResultOf, self.is_result_of.iri))
        for ele in self.is_sample_of:
            g.add((self.iri, SOSA.isSampleOf, ele.iri))

        return g
