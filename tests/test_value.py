from rdflib.namespace import OWL, RDF, SKOS

from client._TERN import TERN
from client.model import Value


def test_basic_rdf():
    r1 = Value()
    rdf = r1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Value) in rdf
