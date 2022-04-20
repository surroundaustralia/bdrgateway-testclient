from typing import Optional, List

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, VOID, SOSA

from client.model._TERN import TERN
from client.model.concept import Concept
from client.model.feature_of_interest import FeatureOfInterest
from client.model.observation import Observation
from client.model.rdf_dataset import RDFDataset
from client.model.site_visit import SiteVisit


class Site(FeatureOfInterest):
    def __init__(
        self,
        is_result_of: Observation,
        is_sample_of: List[FeatureOfInterest],
        in_dataset: RDFDataset,
        feature_type: Concept,
        iri: Optional[str] = None,
        label: Optional[Literal] = None,
        has_site_visit: Optional[SiteVisit] = None,
    ):
        assert isinstance(
            is_result_of.__class__, Observation.__class__
        ), "You must supply an observation for sosa:isResultOf"

        assert len(is_sample_of) >= 1, (
            "You must supply a minimum of 1 Sample object(s)"
            " for the property is_sample_of"
        )

        assert isinstance(
            in_dataset.__class__, RDFDataset.__class__
        ), "The object supplied for the property in_dataset must be of type RDFDataset"

        assert isinstance(
            feature_type.__class__, Concept.__class__
        ), "The object supplied for the property feature_type must be of type Concept"

        if label is not None:
            assert isinstance(
                label.__class__, Literal.__class__
            ), "If you supply a label, it must be an RDFLib Literal"

        if has_site_visit:
            assert isinstance(has_site_visit.__class__, SiteVisit.__class__), \
                    "The object supplied for the property has_site_visit must be of type SiteVisit"

        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/site/{self.id}")

        self.iri = URIRef(iri)
        super().__init__(feature_type, iri)
        self.feature_type = feature_type
        self.in_dataset = in_dataset
        self.is_result_of = is_result_of
        self.is_sample_of = is_sample_of
        if label is None:
            self.label = f"Site with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"
        else:
            self.label = label
        self.has_site_visit = has_site_visit

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
        if (self.in_dataset.iri, RDF.type, None) not in g:
            g += self.in_dataset.to_graph()

        if self.is_result_of is not None:
            g.add((self.iri, SOSA.isResultOf, self.is_result_of.iri))
            if (self.is_result_of.iri, RDF.type, None) not in g:
                g += self.is_result_of.to_graph()
        for ele in self.is_sample_of:
            g.add((self.iri, SOSA.isSampleOf, ele.iri))

        if self.has_site_visit:
            g.add((self.iri, TERN.hasSiteVisit, self.has_site_visit.iri))

        return g
