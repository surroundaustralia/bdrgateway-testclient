from rdflib import Literal, URIRef
from rdflib.namespace import OWL, RDF, XSD

from client._TERN import TERN
from client.model import Concept, FeatureOfInterest, RDFDataset, Sample, Sampling


def test_basic_rdf():
    rdfdataset1 = RDFDataset()
    foi1 = FeatureOfInterest(
        Concept(),
        rdfdataset1,
    )
    results = [Sample([foi1], Concept(), rdfdataset1, None)]
    s1 = Sampling(
        foi1,
        Literal("2001-01-01", datatype=XSD.date),
        URIRef("http://example.com/producure/x"),
        results,
    )
    rdf = s1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Sampling) in rdf
