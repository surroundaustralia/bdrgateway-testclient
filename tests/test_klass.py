from client.model import Klass
from rdflib.namespace import RDF, OWL


def test_basic_rdf():
    r1 = Klass()
    rdf = r1.to_graph()

    assert (None, RDF.type, OWL.Class) in rdf
