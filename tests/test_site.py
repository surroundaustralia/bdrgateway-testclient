from rdflib.namespace import OWL, RDF
from rdflib import Literal
from client._TERN import TERN
from client.model import (
    Concept,
    RDFDataset,
    FeatureOfInterest,
    Sample,
    Sampling,
    Site
)

def test_basic_rdf():
    rdfdataset1 = RDFDataset()
    foi1 = FeatureOfInterest(Concept(), rdfdataset1,)
    sample = Sample([foi1], Concept(), rdfdataset1, None)
    s1 = Site(None, [foi1], rdfdataset1, Literal("label"), Concept())
    rdf = s1.to_graph()
    print(rdf.serialize())

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Site)

