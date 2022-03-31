from client.model import Concept
from rdflib.namespace import OWL, RDF, SKOS


def test_basic_rdf():
    r1 = Concept()
    rdf = r1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, SKOS.Concept) in rdf
