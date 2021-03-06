from rdflib.namespace import OWL, RDF, URIRef

from client.model import (
    RDFDataset,
    Attribute,
    Value,
)
from client.model._TERN import TERN


def test_basic_rdf():
    rdfdataset1 = RDFDataset()
    attribute = URIRef("https://example.org")
    simple_value = URIRef("https://example.org")

    s1 = Attribute(attribute, simple_value, Value(), Value(), rdfdataset1)
    rdf = s1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Attribute) in rdf
