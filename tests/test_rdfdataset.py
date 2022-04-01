from rdflib.namespace import OWL, RDF

from client._TERN import TERN
from client.model import RDFDataset


def test_basic_rdf():
    r1 = RDFDataset()
    rdf = r1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.RDFDataset) in rdf
