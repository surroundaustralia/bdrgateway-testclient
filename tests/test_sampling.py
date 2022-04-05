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
    sample1 = Sample([foi1], Concept(), rdfdataset1, None)
    s1 = Sampling(
        foi1,
        Literal("2001-01-01", datatype=XSD.date),
        URIRef("http://example.com/procedure/x"),
        [sample1],
    )
    sample1.is_result_of = (
        s1  # link the Sample to the Sampling, now that both are declared
    )
    rdf = s1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Sampling) in rdf
