from rdflib import BNode, URIRef
from rdflib.namespace import OWL, RDF, SKOS

from client._TERN import TERN
from client.model import Value


def test_basic_rdf():
    v1 = Value()
    rdf = v1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Value) in rdf


def test_bank_node():
    v1 = Value(is_blank_node=True)
    rdf = v1.to_graph()

    assert (None, RDF.type, TERN.Value) in rdf
    assert type(v1.iri) == BNode, "The type of this Value's IRI should be a BNode"

    v2 = Value(is_blank_node=False)
    rdf = v2.to_graph()

    assert (None, RDF.type, TERN.Value) in rdf
    assert type(v2.iri) == URIRef, "The type of this Value's IRI should be a URIRef"
