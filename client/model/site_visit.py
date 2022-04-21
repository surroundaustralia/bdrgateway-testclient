from typing import Optional

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, VOID, PROV, XSD

from client.model._TERN import TERN
from client.model.klass import Klass
from client.model.rdf_dataset import RDFDataset


class SiteVisit(Klass):
    def __init__(
        self,
        in_dataset: RDFDataset,
        started_at_time: Literal,
        iri: Optional[str] = None,
        label: Optional[Literal] = None,
    ):
        assert (
            type(in_dataset) == RDFDataset
        ), "The object supplied for the property in_dataset must be of type RDFDataset"

        assert (
            type(started_at_time) == Literal
            and started_at_time.datatype == XSD.dateTime
        ), "The value for started_at_time must be an RDFLib Literal with datatype of xsd:dateTime"

        if label is not None:
            assert (
                type(label) == Literal
            ), "If you supply a label, it must be an RDFLib Literal"

        # this is potentially problematic as these sites shouldn't be random
        # But for now will continue and use the same logic as prior
        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/sitevisit/{self.id}")

        self.iri = URIRef(iri)
        super().__init__(iri)
        self.in_dataset = in_dataset
        self.started_at_time = started_at_time

        if label is None:
            self.label = f"SiteVisit with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"
        else:
            self.label = label

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        g.remove((self.iri, RDFS.label, None))

        g.add((self.iri, RDF.type, TERN.SiteVisit))
        g.add((self.iri, RDFS.label, Literal(self.label)))
        g.add((self.iri, VOID.inDataset, self.in_dataset.iri))
        if (self.in_dataset.iri, RDF.type, None) not in g:
            g += self.in_dataset.to_graph()

        return g
