from rdflib import URIRef, Namespace
from rdflib.namespace import OWL, RDF

from client.model import Taxon
from client.model._TERN import TERN

DWC = Namespace("http://rs.tdwg.org/dwc/terms/")


def test_basic_rdf():
    rdf = Taxon(URIRef("http://example.com/scientificNameID/x")).to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Value) in rdf
    assert (None, RDF.type, TERN.Taxon) in rdf


def test_scientific_name():
    sn = URIRef("http://example.com/scientificNameID/x")
    t1 = Taxon(sn)
    rdf = t1.to_graph()

    assert t1.scientific_name_id == sn
    assert (t1.iri, DWC.scientificNameID, sn) in rdf
