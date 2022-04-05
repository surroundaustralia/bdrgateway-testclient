from rdflib import Literal
from rdflib.namespace import OWL, RDF, XSD

from client.model import RDFDataset, SiteVisit
from client.model._TERN import TERN


def test_basic_rdf():
    sv1 = SiteVisit(RDFDataset(), Literal("2001-01-01T00:00:01", datatype=XSD.dateTime))
    rdf = sv1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.SiteVisit)
