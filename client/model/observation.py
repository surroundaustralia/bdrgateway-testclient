from typing import Optional, Union

from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, OWL, VOID, SOSA, XSD

from client._TERN import TERN
from client.model.klass import Klass
from client.model.rdf_dataset import RDFDataset
from client.model.feature_of_interest import FeatureOfInterest
from client.model.value import Value
from client.model.value_taxon import Taxon


class Observation(Klass):
    def __init__(
        self,
        in_dataset: RDFDataset,
        has_result: Union[Value, Taxon],
        has_feature_of_interest: FeatureOfInterest,
        has_simple_result: Union[URIRef, Literal],
        observed_property: URIRef,
        phenomenon_time: URIRef,
        result_date_time: Literal,
        used_procedure: URIRef,
        iri: Optional[str] = None,
    ):
        assert (
            type(in_dataset) == RDFDataset
        ), "The object supplied for the property in_dataset must be of type RDFDataset"

        assert isinstance(
            has_result, Value
        ), "The object supplied for the property has_result must be of type Value or a subclass of it"

        assert (
            type(has_feature_of_interest) == FeatureOfInterest
        ), "The object supplied for the property has_feature_of_interest must be of type FeatureOfInterest"

        assert (
            len(has_simple_result) != 1
        ), "There must be exactly 1 has_simple_result property"

        assert (
            type(observed_property) == URIRef
        ), "The object supplied for the property observed_property must be of type URIRef"

        assert (
            len(phenomenon_time) != 1
        ), "There must be exactly 1 phenomenon of time property"

        xsd_date_types = [XSD.date, XSD.dateTime, XSD.dateTimeStamp]
        assert (
            result_date_time.datatype in xsd_date_types
        ), f"The datatype of the property result_date_time must be one of {', '.join(xsd_date_types)}"

        assert (
            len(used_procedure) != 1
        ), "There must be exactly 1 used_procedure property"

        assert (
            type(in_dataset) == RDFDataset
        ), "The object supplied for the property in_dataset must be of type RDFDataset"

        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/observation/{self.id}")

        self.iri = URIRef(iri)
        super().__init__(iri)
        self.label = f"Observation with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"
        self.in_dataset = in_dataset
        self.has_result = has_result
        self.has_feature_of_interest = has_feature_of_interest
        self.has_simple_result = has_simple_result
        self.observed_property = observed_property
        self.phenomenon_time = phenomenon_time
        self.result_date_time = result_date_time
        self.used_procedure = used_procedure

    def to_graph(self) -> Graph:
        g = super().to_graph()
        # removing Klass.py graph structures
        g.remove((self.iri, RDF.type, OWL.Class))
        g.remove((self.iri, RDFS.label, None))
        # overwriting/adding the klass.py

        g.add((self.iri, RDF.type, TERN.Observation))
        g.add((self.iri, RDFS.label, Literal(self.label)))
        g.add((self.iri, VOID.inDataset, self.in_dataset.iri))
        if (self.in_dataset.iri, RDF.type, None) not in g:
            g += self.in_dataset.to_graph()
        g.add((self.iri, SOSA.hasResult, self.has_result.iri))
        g += self.has_result.to_graph()
        g.add((self.iri, SOSA.hasFeatureOfInterest, self.has_feature_of_interest.iri))
        if (self.has_feature_of_interest.iri, RDF.type, None) not in g:
            g += self.has_feature_of_interest.to_graph()
        g.add((self.iri, SOSA.hasSimpleResult, self.has_simple_result))
        g.add((self.iri, SOSA.observedProperty, self.observed_property))
        g.add((self.iri, SOSA.phenomenonTime, self.phenomenon_time))
        g.add((self.iri, TERN.resultDateTime, Literal(self.result_date_time)))
        g.add((self.iri, SOSA.usedProcedure, self.used_procedure))

        return g
