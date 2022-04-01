from rdflib.namespace import OWL, RDF

from client._TERN import TERN
from client.model import (
    Concept,
    RDFDataset,
    FeatureOfInterest,
    Sample,
)


def test_basic_rdf():
    rdfdataset1 = RDFDataset()
    foi1 = FeatureOfInterest(
        Concept(),
        rdfdataset1,
    )
    s1 = Sample([foi1], Concept(), rdfdataset1, None)
    rdf = s1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Sample) in rdf
