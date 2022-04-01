from rdflib.namespace import OWL, RDF, SKOS

from client.model import Concept


def test_basic_rdf():
    r1 = Concept()
    rdf = r1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, SKOS.Concept) in rdf
