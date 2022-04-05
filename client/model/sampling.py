from typing import List, Optional

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SOSA, OWL, XSD

from client._TERN import TERN
from client.model.feature_of_interest import FeatureOfInterest
from client.model.klass import Klass
from client.model.sample import Sample


class Sampling(Klass):
    def __init__(
        self,
        has_feature_of_interest: FeatureOfInterest,
        result_date_time: Literal,
        used_procedure: URIRef,
        has_result: List[Sample],
        iri: Optional[str] = None,
    ):
        assert (
            type(has_feature_of_interest) == FeatureOfInterest
        ), "The object supplied for the property has_feature_of_interest must be of type FeatureOfInterest"

        assert (
            type(result_date_time) == Literal
        ), "The object supplied for the property result_date_time must be of type Literal"

        xsd_date_types = [XSD.date, XSD.dateTime, XSD.dateTimeStamp]
        assert (
            result_date_time.datatype in xsd_date_types
        ), f"The datatype of the property result_date_time must be one of {', '.join(xsd_date_types)}"

        assert (
            type(used_procedure) == URIRef
        ), "The object supplied for the property used_procedure must be of type URIRef"

        assert (
            len(has_result) >= 1
        ), "You must supply a minimum of 1 Sample objects for the property has_result"

        assert all(
            type(el) == Sample for el in has_result
        ), "Every object supplied in the property has_result list must be of type Sample"

        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/sampling/{self.id}")

        self.iri = URIRef(iri)

        super().__init__(iri)

        self.label = f"Sampling with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"

        self.result_date_time = result_date_time
        self.used_procedure = used_procedure
        self.has_result = has_result
        self.has_feature_of_interest = has_feature_of_interest

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        g.add((self.iri, RDF.type, TERN.Sampling))
        g.remove((self.iri, RDFS.label, None))
        g.add((self.iri, SOSA.hasFeatureOfInterest, self.has_feature_of_interest.iri))
        g.add((self.iri, RDFS.label, Literal(self.label)))
        g.add((self.iri, TERN.resultDateTime, self.result_date_time))
        g.add((self.iri, SOSA.usedProcedure, self.used_procedure))
        for result in self.has_result:
            g.add((self.iri, SOSA.hasResult, result.iri))

        return g
