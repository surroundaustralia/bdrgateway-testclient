from typing import Optional, Union

from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, OWL, VOID, SOSA, TIME, XSD

from client.model._TERN import TERN
from client.model.feature_of_interest import FeatureOfInterest
from client.model.klass import Klass
from client.model.rdf_dataset import RDFDataset
from client.model.value import Value
from client.model.value_taxon import Taxon
from client.model.site_visit import SiteVisit


class Observation(Klass):
    def __init__(
        self,
        in_dataset: RDFDataset,
        has_result: Union[Value, Taxon],
        has_feature_of_interest: Union[FeatureOfInterest, "Sample"],
        has_simple_result: Union[URIRef, Literal],
        observed_property: URIRef,
        phenomenon_time: URIRef,
        result_date_time: Literal,
        used_procedure: URIRef,
        iri: Optional[str] = None,
        has_site_visit: Optional[SiteVisit] = None,
    ):
        assert isinstance(
            in_dataset.__class__, RDFDataset.__class__
        ), "The object supplied for the property in_dataset must be of type RDFDataset"

        assert isinstance(
            has_result.__class__, Value.__class__
        ), "The object supplied for the property has_result must be of type Value or a subclass of it"

        assert isinstance(
            has_feature_of_interest.__class__, FeatureOfInterest.__class__
        ), "The object supplied for the property has_feature_of_interest must be of type FeatureOfInterest"

        simple_result_types = [URIRef, Literal]
        assert has_simple_result.__class__ in simple_result_types, "There must be exactly 1 has_simple_result property and it must be either a URIRef or a Literal"

        assert isinstance(
            observed_property.__class__, URIRef.__class__
        ), "The object supplied for the property observed_property must be of type URIRef"

        assert (
            len(phenomenon_time) != 1
        ), "There must be exactly 1 phenomenon of time property"

        xsd_date_types = [XSD.date, XSD.dateTime, XSD.dateTimeStamp]
        assert (
            result_date_time.datatype in xsd_date_types
        ), f"The datatype of the property result_date_time must be one of {', '.join(xsd_date_types)}"

        assert (
            isinstance(used_procedure.__class__, URIRef.__class__)
        ), "There must be exactly 1 used_procedure property"

        assert isinstance(
            in_dataset.__class__, RDFDataset.__class__
        ), "The object supplied for the property in_dataset must be of type RDFDataset"

        if has_site_visit:
            assert isinstance(has_site_visit.__class__, SiteVisit.__class__), \
                    "The object supplied for the property has_site_visit must be of type SiteVisit" \
                    "and has a maximum of 1 supplied properties"

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
        self.has_site_visit = has_site_visit

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
        t = BNode()
        g.add((self.iri, SOSA.phenomenonTime, self.phenomenon_time))
        g.add((self.phenomenon_time, RDF.type, TIME.Instant))
        g.add((self.phenomenon_time, TIME.inXSDDate, Literal("2001-01-01", datatype=XSD.date)))
        g.add((self.iri, TERN.resultDateTime, Literal(self.result_date_time)))
        g.add((self.iri, SOSA.usedProcedure, self.used_procedure))
        if self.has_site_visit:
            g.add((self.iri, TERN.hasSiteVisit, self.has_site_visit.iri))
            if (self.has_site_visit.iri, RDF.type, None) not in g:
                g += self.has_site_visit.to_graph()

        return g
