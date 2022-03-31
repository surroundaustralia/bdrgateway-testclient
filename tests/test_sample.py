from client.model import Concept, RDFDataset, Sample
from rdflib.namespace import OWL, RDF
from client._TERN import TERN


def test_basic_rdf():
    r1 = RDFDataset()
    c1 = Concept()
    s1 = Sample(r1, c1)
    rdf = s1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Sample) in rdf
