from rdflib import URIRef, Literal, Namespace
from rdflib.namespace import OWL, RDF, XSD

from client.model import Float
from client.model._TERN import TERN

DWC = Namespace("http://rs.tdwg.org/dwc/terms/")


def test_basic_rdf():
    rdf = Float(Literal(42, datatype=XSD.double)).to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Value) not in rdf
    assert (None, RDF.type, TERN.Float) in rdf


def test_value_unit():
    v = Literal(42, datatype=XSD.double)
    u = URIRef("http://qudt.org/vocab/unit/CentiM")
    f = Float(v, u)
    rdf = f.to_graph()

    assert (f.iri, RDF.value, v) in rdf
    assert (f.iri, TERN.unit, u) in rdf
