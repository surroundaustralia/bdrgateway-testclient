from rdflib.namespace import OWL, RDF, XSD
from rdflib import Literal
from client._TERN import TERN
from client.model import (
    RDFDataset,
    SiteVisit
)


def test_basic_rdf():
    sv1 = SiteVisit(RDFDataset(), Literal("2001-01-01T00:00:01", datatype=XSD.dateTime))
    rdf = sv1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.SiteVisit)
