from typing import Optional

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS, VOID, XSD, PROV

from client.model._TERN import TERN
from client.model.klass import Klass
from client.model.rdf_dataset import RDFDataset


class HasSiteVisit(Klass):
    def __init__(
            self,
            in_dataset: RDFDataset,
            started_at_time: Literal,
            iri: Optional[str] = None,
    ):
        assert isinstance(
            in_dataset.__class__, RDFDataset.__class__
        ), "The object supplied for the property in_dataset must be of type RDFDataset"

        xsd_date_types = [XSD.date, XSD.dateTime, XSD.dateTimeStamp]
        assert (
                started_at_time.datatype in xsd_date_types
        ), f"The datatype of the property started_at_time must be one of {', '.join(xsd_date_types)}"

        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/has_site_visit/{self.id}")

        self.iri = URIRef(iri)

        super(HasSiteVisit, self).__init__(iri)

        self.label = f"A Site Visit with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"

        self.in_dataset = in_dataset
        self.started_at_time = started_at_time

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        g.remove((self.iri, RDFS.label, None))

        g.add((self.iri, RDF.type, TERN.hasSiteVisit))
        g.add((self.iri, RDFS.label, Literal(self.label)))


        g.add((self.iri, VOID.inDataset, self.in_dataset.iri))
        g.add((self.iri, PROV.startedAtTime, Literal(self.started_at_time)))

        return g
