from client.model.dataset import RDFDataset
from rdflib.namespace import RDF
from client._TERN import TERN


def test_basic_rdf():
    r1 = RDFDataset()
    rdf = r1.to_graph()

    assert (None, RDF.type, TERN.RDFDataset) in rdf
