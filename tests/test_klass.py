from rdflib.namespace import RDF, OWL

from client.model import Klass


def test_basic_rdf():
    r1 = Klass()
    rdf = r1.to_graph()

    assert (None, RDF.type, OWL.Class) in rdf
