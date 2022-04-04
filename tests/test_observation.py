from rdflib.namespace import OWL, RDF, URIRef, XSD
from rdflib import Literal, URIRef
from client._TERN import TERN
from client.model import (
    Concept,
    RDFDataset,
    FeatureOfInterest,
    Sample,
    Site,
    Attribute,
    Value,
    Observation
)


# TODO: Confirm this testing is sufficient
def test_basic_rdf():
    rdfdataset1 = RDFDataset()
    has_result = URIRef("https://example.org")
    foi1 = FeatureOfInterest(Concept(), rdfdataset1, )

    s1 = Observation(rdfdataset1,
                     has_result,
                     foi1,
                     "https://example.com",
                     foi1,
                     URIRef("http://example.com"),
                     Literal("2001-01-01", datatype=XSD.date),
                     URIRef("https://example.com/procedure/x/"))
    rdf = s1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Observation)
