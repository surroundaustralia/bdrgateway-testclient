from rdflib import URIRef, Literal, Namespace
from rdflib.namespace import OWL, RDF, SKOS

from client._TERN import TERN
from client.model import Taxon

DWC = Namespace("http://rs.tdwg.org/dwc/terms/")


def test_basic_rdf():
    rdf = Taxon(
        URIRef("http://example.com/scientificNameID/x")
    ).to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Value) not in rdf
    assert (None, RDF.type, TERN.Taxon) in rdf


def test_scientific_name():
    sn = URIRef("http://example.com/scientificNameID/x")
    t1 = Taxon(sn)
    rdf = t1.to_graph()

    assert t1.scientific_name_id == sn
    assert (t1.iri, DWC.scientificNameID, sn) in rdf
