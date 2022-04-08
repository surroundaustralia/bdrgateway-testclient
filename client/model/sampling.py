from typing import List, Optional, Tuple

from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF, RDFS, SOSA, OWL, XSD

GEO = Namespace("http://www.opengis.net/ont/geosparql#")

from client.model._TERN import TERN
from client.model.feature_of_interest import FeatureOfInterest
from client.model.klass import Klass
from client.model.sample import Sample
from shapely.geometry import Point


class Sampling(Klass):
    def __init__(
        self,
        has_feature_of_interest: FeatureOfInterest,
        result_date_time: Literal,
        used_procedure: URIRef,
        has_result: List[Sample] = [],
        iri: Optional[str] = None,
        geometry: Optional[Point] = None
    ):
        assert isinstance(
            has_feature_of_interest.__class__, FeatureOfInterest.__class__
        ), "The object supplied for the property has_feature_of_interest must be of type FeatureOfInterest"

        assert isinstance(
            result_date_time.__class__, Literal.__class__
        ), "The object supplied for the property result_date_time must be of type Literal"

        xsd_date_types = [XSD.date, XSD.dateTime, XSD.dateTimeStamp]
        assert (
            result_date_time.datatype in xsd_date_types
        ), f"The datatype of the property result_date_time must be one of {', '.join(xsd_date_types)}"

        assert isinstance(
            used_procedure.__class__, URIRef.__class__
        ), "The object supplied for the property used_procedure must be of type URIRef"

        # assert (
        #     len(has_result) >= 1
        # ), "You must supply a minimum of 1 Sample objects for the property has_result"

        if len(has_result) > 0:
            assert all(
                isinstance(el.__class__, Sample.__class__) for el in has_result
            ), "Every value supplied for has_result must be of type Sample"

        if geometry is not None:
            assert isinstance(geometry.__class__, Point.__class__), \
                "If a coordinate is supplied, it must be a Point"

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
        self.geometry = geometry

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        g.add((self.iri, RDF.type, TERN.Sampling))
        g.remove((self.iri, RDFS.label, None))
        g.add((self.iri, SOSA.hasFeatureOfInterest, self.has_feature_of_interest.iri))
        if (self.has_feature_of_interest.iri, RDF.type, None) not in g:
            g += self.has_feature_of_interest.to_graph()
        g.add((self.iri, RDFS.label, Literal(self.label)))
        g.add((self.iri, TERN.resultDateTime, self.result_date_time))
        g.add((self.iri, SOSA.usedProcedure, self.used_procedure))
        for result in self.has_result:
            g.add((self.iri, SOSA.hasResult, result.iri))
            # if (result.iri, RDF.type, None) not in g:
            #     g += result.to_graph()
        if self.geometry:
            geom_iri = URIRef(self.iri + "/geom")
            g.add((self.iri, GEO.hasGeometry, geom_iri))
            g.add((geom_iri, RDF.type, GEO.Geometry))
            g.add((geom_iri, GEO.asWKT, Literal(self.geometry.wkt, datatype=GEO.wktLiteral)))

        return g
