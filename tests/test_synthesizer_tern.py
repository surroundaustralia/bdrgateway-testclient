from client.synthesizer_tern import TernSynthesizer
from shapely.geometry import box
from client.model._TERN import TERN
from rdflib.namespace import RDF
from rdflib import Namespace
GEO = Namespace("http://www.opengis.net/ont/geosparql#")


def test_samplings_count():
    # Geralton to Esperance
    synth = TernSynthesizer(3, box(115.992191, -33.871399, 121.9467547, -28.572837))
    g = synth.to_graph()
    assert len(list(g.subjects(RDF.type, TERN.Sampling))) == 3


def test_coordinates():
    # Geralton to Esperance
    synth = TernSynthesizer(10, box(115.992191, -33.871399, 121.9467547, -28.572837))
    for coord in synth.coordinate_points:
        assert 115.992191 < coord.x < 121.9467547 and -33.871399 < coord.y < -28.572837